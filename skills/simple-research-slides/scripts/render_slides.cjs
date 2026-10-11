#!/usr/bin/env node
// Export the companion local HTML template; no installs or machine configuration.
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');

function parseArgs(argv) {
  let file, outDir, strict = false;
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--out-dir') {
      if (!argv[i + 1] || argv[i + 1].startsWith('--')) throw new Error('--out-dir needs a directory');
      outDir = path.resolve(argv[++i]);
    } else if (arg === '--strict') strict = true;
    else if (arg.startsWith('--') || file) throw new Error(`Unexpected argument: ${arg}`);
    else file = path.resolve(arg);
  }
  if (!file || !outDir || path.extname(file).toLowerCase() !== '.html') {
    throw new Error('Usage: node render_slides.cjs FILE.html --out-dir DIR [--strict]');
  }
  if (!fs.statSync(file).isFile()) throw new Error('Expected a local HTML file');
  if (fs.existsSync(path.join(outDir, 'render-check.json'))) {
    throw new Error('Output directory already contains a render; choose a new version directory');
  }
  return {file, outDir, strict};
}

// Called in the browser after fonts and images have loaded.
function auditSlide(index) {
  const slide = document.querySelectorAll('.slide')[index];
  const root = slide.getBoundingClientRect();
  const visible = element => {
    const style = getComputedStyle(element), box = element.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && box.width > 0 && box.height > 0;
  };
  const elements = [...slide.querySelectorAll('[data-qa]')].filter(visible);
  const describe = el => (el.textContent.trim() || el.getAttribute('aria-label') || el.tagName).slice(0, 120);
  const boxes = elements.map(el => ({el, box: el.getBoundingClientRect()}));
  const outside = boxes.filter(({box: b}) => b.left < root.left - 1 || b.top < root.top - 1 || b.right > root.right + 1 || b.bottom > root.bottom + 1).map(({el}) => describe(el));
  const overflow = elements.filter(el => el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2).map(describe);
  const overlaps = [];
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const a = boxes[i], b = boxes[j];
    if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
    if (Math.min(a.box.right, b.box.right) - Math.max(a.box.left, b.box.left) > 2 &&
        Math.min(a.box.bottom, b.box.bottom) - Math.max(a.box.top, b.box.top) > 2) {
      overlaps.push({first: describe(a.el), second: describe(b.el)});
    }
  }
  const unloadedImages = [...slide.querySelectorAll('img')].filter(im => !im.complete || !im.naturalWidth).map(im => im.getAttribute('src')?.slice(0, 120));
  return {slide: index + 1, title: slide.dataset.title || '', checkedElements: elements.length,
    bounds: {width: root.width, height: root.height}, outside, overflow, overlaps, unloadedImages};
}

async function main() {
  const {file, outDir, strict} = parseArgs(process.argv.slice(2));
  const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
  const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || undefined,
    headless: true, args: process.env.CHROMIUM_NO_SANDBOX === '1' ? ['--no-sandbox'] : []});
  fs.mkdirSync(outDir, {recursive: true});
  const report = {source: path.basename(file), slides: [], blockedRequests: [], pageErrors: [],
    checks: {}, limitations: 'Marked-element boxes only. Does not prove glyph legibility, image-internal text, font identity, scientific correctness, or absence of every collision. Inspect actual PNG and PDF pages.'};
  let context;
  try {
    context = await browser.newContext({viewport: {width: 1280, height: 720}, deviceScaleFactor: 1});
    const page = await context.newPage();
    page.on('pageerror', error => report.pageErrors.push(error.message));
    await page.route(/^https?:\/\//, route => {report.blockedRequests.push(route.request().url()); return route.abort();});
    await page.goto(pathToFileURL(file).href, {waitUntil: 'load'});
    await page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.all([...document.images].map(image => image.decode().catch(() => undefined)));
    });
    const count = await page.locator('.slide').count();
    const apiValid = await page.evaluate(count => typeof window.simpleSlides?.show === 'function' && window.simpleSlides.count === count, count);
    if (!count || !apiValid) throw new Error('Expected .slide elements and matching window.simpleSlides API');
    report.slideCount = count;
    for (let i = 0; i < count; i++) {
      await page.evaluate(i => {window.simpleSlides.show(i); document.body.classList.add('qa');}, i);
      report.slides.push(await page.evaluate(auditSlide, i));
      await page.screenshot({path: path.join(outDir, `slide-${String(i + 1).padStart(2, '0')}.png`)});
    }
    report.checks.fontsLoaded = await page.evaluate(() => document.fonts.status === 'loaded');
    await page.evaluate(() => {document.body.classList.remove('qa'); window.simpleSlides.show(0);});
    await page.keyboard.press('ArrowRight');
    report.checks.keyboardNavigation = await page.evaluate(expected => window.simpleSlides.index === expected, Math.min(1, count - 1));
    await page.keyboard.press('n');
    report.checks.notesToggle = await page.evaluate(() => {
      const panel = document.getElementById('note-panel');
      return document.body.classList.contains('notes-on') && !!panel?.textContent.trim() && getComputedStyle(panel).display !== 'none';
    });
    await page.setViewportSize({width: 960, height: 540});
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    report.checks.viewportFit = await page.evaluate(() => {
      const rect = document.querySelector('.slide.active').getBoundingClientRect();
      return rect.left >= -1 && rect.top >= -1 && rect.right <= innerWidth + 1 && rect.bottom <= innerHeight + 1;
    });
    const notes = await page.evaluate(() => [...document.querySelectorAll('.slide')].map((slide, i) => ({
      slide: i + 1, title: slide.dataset.title || '', seconds: slide.dataset.seconds ? Number(slide.dataset.seconds) : null,
      notes: slide.querySelector('.notes')?.textContent.trim() || ''
    })));
    report.checks.allSlidesHaveNotes = notes.every(note => !!note.notes);
    const timed = notes.filter(n => n.seconds !== null);
    report.timing = {timedSlideCount: timed.length, seconds: timed.reduce((sum, n) => sum + n.seconds, 0)};
    if (timed.some(n => !Number.isFinite(n.seconds) || n.seconds < 0)) throw new Error('Invalid data-seconds value');
    fs.writeFileSync(path.join(outDir, 'speaker-notes.md'), notes.map(n => `## ${n.slide}. ${n.title}\n\n${n.seconds === null ? '时间未设置' : `建议时间：${n.seconds}秒`}\n\n${n.notes}\n`).join('\n'));
    await page.emulateMedia({media: 'print'});
    await page.evaluate(() => document.fonts.ready);
    report.printSlides = [];
    for (let i = 0; i < count; i++) report.printSlides.push(await page.evaluate(auditSlide, i));
    report.checks.printSlidesVisible = await page.evaluate(() => [...document.querySelectorAll('.slide')].every(s => getComputedStyle(s).display !== 'none'));
    report.checks.printControlsHidden = await page.evaluate(() => [...document.querySelectorAll('.controls,.note-panel')].every(el => getComputedStyle(el).display === 'none'));
    await page.pdf({path: path.join(outDir, 'slides.pdf'), printBackground: true, preferCSSPageSize: true});
    const records = [...report.slides, ...report.printSlides];
    const hardFailure = report.blockedRequests.length || report.pageErrors.length || records.some(s => s.outside.length || s.overflow.length || s.unloadedImages.length || !s.checkedElements) || Object.values(report.checks).some(passed => !passed);
    const needsReview = records.some(s => s.overlaps.length);
    report.status = hardFailure ? 'FIX BEFORE DELIVERY' : needsReview ? 'REVIEW REQUIRED' : 'AUTOMATED CHECKS PASSED';
    if (hardFailure || (strict && needsReview)) process.exitCode = 1;
  } catch (error) {
    report.error = error.message;
    report.status = 'FIX BEFORE DELIVERY';
    process.exitCode = 1;
  } finally {
    fs.writeFileSync(path.join(outDir, 'render-check.json'), JSON.stringify(report, null, 2) + '\n');
    if (context) await context.close();
    await browser.close();
  }
  console.log(`${path.basename(file)}: ${report.status}${report.error ? ' · ' + report.error : ''}`);
}

main().catch(error => {console.error(error.message); process.exitCode = 1;});
