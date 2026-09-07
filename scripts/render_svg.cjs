#!/usr/bin/env node
// Print self-contained SVGs as native PDF; inspect transformed text in page pixels.
const fs = require('node:fs');
const path = require('node:path');

function parseArgs(argv) {
  const files = [];
  let outDir;
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--out-dir') {
      if (!argv[i + 1]) throw new Error('--out-dir needs a directory');
      outDir = path.resolve(argv[++i]);
    } else if (argv[i].startsWith('--')) {
      throw new Error(`Unknown option: ${argv[i]}`);
    } else files.push(path.resolve(argv[i]));
  }
  if (!files.length) throw new Error('Usage: node render_svg.cjs FILE.svg [...] [--out-dir DIRECTORY]');
  const jobs = files.map(file => {
    if (path.extname(file).toLowerCase() !== '.svg') throw new Error(`Expected an SVG: ${file}`);
    return {file, stem: path.join(outDir || path.dirname(file), path.basename(file, path.extname(file)))};
  });
  if (new Set(jobs.map(j => j.stem)).size !== jobs.length) {
    throw new Error('Output names collide; use distinct SVG basenames or output directories');
  }
  return jobs;
}

async function main() {
  const jobs = parseArgs(process.argv.slice(2));
  const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || undefined,
    headless: true,
    args: process.env.CHROMIUM_NO_SANDBOX === '1' ? ['--no-sandbox'] : [],
  });
  let failed = false;
  try {
    const context = await browser.newContext({javaScriptEnabled: false});
    for (const {file, stem} of jobs) {
      fs.mkdirSync(path.dirname(stem), {recursive: true});
      const page = await context.newPage();
      const blocked = [];
      const report = {source: path.basename(file), coordinate_system: 'Rendered page pixels with ancestor transforms',
        limitations: 'Does not detect all overlaps, nested clipping, missing glyphs or scientific errors.'};
      await page.route('**/*', route => {
        blocked.push(route.request().url());
        return route.abort();
      });
      try {
        const markup = fs.readFileSync(file, 'utf8');
        const dimensions = await page.evaluate(svg => {
          const doc = new DOMParser().parseFromString(svg, 'image/svg+xml');
          if (doc.querySelector('parsererror') || doc.documentElement.localName !== 'svg') {
            throw new Error('Malformed SVG');
          }
          const root = doc.documentElement;
          const vb = (root.getAttribute('viewBox') || '').trim().split(/[\s,]+/).map(Number);
          if (vb.length !== 4 || !vb.every(Number.isFinite) || vb[2] <= 0 || vb[3] <= 0) {
            throw new Error('SVG needs a numeric, positive viewBox');
          }
          const external = [...root.querySelectorAll('image,use')].map(e =>
            e.getAttribute('href') || e.getAttributeNS('http://www.w3.org/1999/xlink', 'href') || '')
            .filter(href => href && !href.startsWith('#') && !href.startsWith('data:'));
          if (external.length) throw new Error('Inline image/use assets before rendering; external references found');
          if (root.querySelector('script,foreignObject') || [...root.querySelectorAll('*')].some(e =>
            [...e.attributes].some(a => /^on/i.test(a.name)))) {
            throw new Error('Expected a static SVG without scripts, event handlers or foreignObject');
          }
          return {width: Math.ceil(vb[2]), height: Math.ceil(vb[3])};
        }, markup);
        const {width, height} = dimensions;
        if (width > 10000 || height > 10000) throw new Error('Preview dimensions exceed 10000 units; scale the viewBox for rendering');
        await page.setViewportSize({width, height});
        await page.setContent(`<html><head><style>@page{size:${width}px ${height}px;margin:0}` +
          `html,body{margin:0;width:${width}px;height:${height}px;background:white}` +
          `body>svg{display:block;width:${width}px;height:${height}px}</style></head><body>${markup}</body></html>`);
        await page.evaluate(() => document.fonts.ready);
        report.dimensions = dimensions;
        report.panel_titles = await page.locator('.panel-title').allTextContents();
        report.canvas_overflow = await page.locator('svg text').evaluateAll((nodes, bounds) =>
          nodes.filter(n => {
            const b = n.getBoundingClientRect();
            return b.width > 0 && b.height > 0 &&
              (b.left < -0.5 || b.top < -0.5 || b.right > bounds.width + 0.5 || b.bottom > bounds.height + 0.5);
          }).map(n => ({text: n.textContent, bounds: n.getBoundingClientRect().toJSON()})), dimensions);
        report.blocked_requests = blocked;
        await page.screenshot({path: stem + '.png'});
        await page.pdf({path: stem + '.pdf', printBackground: true, preferCSSPageSize: true});
        if (report.canvas_overflow.length || blocked.length) failed = true;
      } catch (error) {
        report.error = error.message;
        failed = true;
      } finally {
        fs.writeFileSync(stem + '.render-check.json', JSON.stringify(report, null, 2) + '\n');
        await page.close();
      }
      console.log(`${path.basename(file)}: ${report.error || `${report.canvas_overflow.length} text overflows; ${blocked.length} blocked requests`}`);
    }
    await context.close();
  } finally {
    await browser.close();
  }
  if (failed) process.exitCode = 1;
}

main().catch(error => {console.error(error.message); process.exitCode = 1;});
