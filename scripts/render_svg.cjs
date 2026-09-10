#!/usr/bin/env node
// Native SVG export with final-size text checks; no network or drawing dependencies added.
const fs = require('node:fs');
const path = require('node:path');

function parseArgs(argv) {
  const files = [];
  let outDir, widthMm;
  let minFontPt = 7, strict = false;
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--out-dir') {
      if (!argv[i + 1] || argv[i + 1].startsWith('--')) throw new Error('--out-dir needs a directory');
      outDir = path.resolve(argv[++i]);
    } else if (arg === '--width-mm' || arg === '--min-font-pt') {
      const value = Number(argv[++i]);
      if (!Number.isFinite(value) || value <= 0) throw new Error(`${arg} needs a positive finite number`);
      if (arg === '--width-mm') widthMm = value;
      else minFontPt = value;
    } else if (arg === '--strict') strict = true;
    else if (arg.startsWith('--')) throw new Error(`Unknown option: ${arg}`);
    else files.push(path.resolve(arg));
  }
  if (!files.length) throw new Error('Usage: node render_svg.cjs FILE.svg [...] [--out-dir DIR] [--width-mm N] [--min-font-pt N] [--strict]');
  if (argv.includes('--min-font-pt') && widthMm === undefined) throw new Error('--min-font-pt requires --width-mm');
  const jobs = files.map(file => {
    if (path.extname(file).toLowerCase() !== '.svg') throw new Error(`Expected an SVG: ${file}`);
    return {file, stem: path.join(outDir || path.dirname(file), path.basename(file, path.extname(file)))};
  });
  if (new Set(jobs.map(j => j.stem)).size !== jobs.length) {
    throw new Error('Output names collide; use distinct SVG basenames or output directories');
  }
  return {jobs, widthMm, minFontPt, strict};
}

async function main() {
  const {jobs, widthMm, minFontPt, strict} = parseArgs(process.argv.slice(2));
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
      const report = {source: path.basename(file), coordinate_system: 'Rendered page CSS pixels with ancestor transforms',
        limitations: 'Text-box overlaps are heuristic. Does not audit text/mark collisions, all clipping, actual glyph outlines, font substitution, panel alignment, raster DPI or scientific validity.'};
      await page.route('**/*', route => {
        blocked.push(route.request().url());
        return route.abort();
      });
      try {
        const markup = fs.readFileSync(file, 'utf8');
        const dimensions = await page.evaluate(svg => {
          const doc = new DOMParser().parseFromString(svg, 'image/svg+xml');
          if (doc.querySelector('parsererror') || doc.documentElement.localName !== 'svg') throw new Error('Malformed SVG');
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
          return {width: vb[2], height: vb[3]};
        }, markup);
        const {width, height} = dimensions;
        if (width > 10000 || height > 10000) throw new Error('Preview dimensions exceed 10000 units; scale the viewBox for rendering');
        await page.setViewportSize({width: Math.ceil(width), height: Math.ceil(height)});
        await page.setContent(`<html><head><style>@page{size:${width}px ${height}px;margin:0}` +
          `html,body{margin:0;width:${width}px;height:${height}px;background:white}` +
          `body>svg{display:block;width:${width}px;height:${height}px}</style></head><body>${markup}</body></html>`);
        await page.evaluate(() => document.fonts.ready);
        // Preserve the original-resolution PNG preview; physical size applies to the PDF.
        await page.screenshot({path: stem + '.png'});
        if (widthMm !== undefined) {
          const heightMm = widthMm * height / width;
          if (Math.max(widthMm, heightMm) * 96 / 25.4 > 10000) throw new Error('Final dimensions exceed 10000 CSS pixels');
          await page.evaluate(css => {
            const style = document.createElement('style');
            style.textContent = css;
            document.head.appendChild(style);
          }, `@page{size:${widthMm}mm ${heightMm}mm;margin:0}` +
            `html,body,body>svg{width:${widthMm}mm!important;height:${heightMm}mm!important}`);
          await page.setViewportSize({width: Math.ceil(widthMm * 96 / 25.4), height: Math.ceil(heightMm * 96 / 25.4)});
          report.final_size = {width_mm: widthMm, height_mm: heightMm};
        }
        // Audit the print-media layout, not just a large screen preview.
        await page.emulateMedia({media: 'print'});
        await page.evaluate(() => document.fonts.ready);
        report.dimensions = dimensions;
        report.panel_titles = await page.locator('.panel-title').allTextContents();
        Object.assign(report, await page.evaluate(({widthMm, minFontPt}) => {
          const root = document.querySelector('body>svg');
          const bounds = root.getBoundingClientRect();
          const visible = n => {
            const s = getComputedStyle(n), b = n.getBoundingClientRect();
            return s.visibility !== 'hidden' && s.display !== 'none' && b.width > 0 && b.height > 0;
          };
          const texts = [...root.querySelectorAll('text')].filter(visible);
          const boxes = texts.map(n => ({text: n.textContent, bounds: n.getBoundingClientRect().toJSON()}));
          const canvas_overflow = boxes.filter(({bounds: b}) =>
            b.left < bounds.left - 0.5 || b.top < bounds.top - 0.5 || b.right > bounds.right + 0.5 || b.bottom > bounds.bottom + 0.5);
          const text_collisions = [];
          for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
            const a = boxes[i].bounds, b = boxes[j].bounds;
            if (Math.min(a.right, b.right) - Math.max(a.left, b.left) > 0.5 &&
                Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 0.5) {
              text_collisions.push({first: boxes[i].text, second: boxes[j].text});
            }
          }
          const font_check = {status: 'NOT REQUESTED', threshold_pt: minFontPt, minimum_pt: null, small_text: []};
          if (widthMm !== undefined) {
            const sizes = [...root.querySelectorAll('text,tspan')].filter(n => visible(n) &&
              [...n.childNodes].some(c => c.nodeType === Node.TEXT_NODE && c.textContent.trim())).map(n => {
              const m = n.getScreenCTM();
              const s = getComputedStyle(n);
              // Smallest singular value includes rotation, skew and anisotropic scaling.
              const sum = m.a*m.a + m.b*m.b + m.c*m.c + m.d*m.d;
              const det = m.a*m.d - m.b*m.c;
              const scale = Math.sqrt(Math.max(0, (sum - Math.sqrt(Math.max(0, sum*sum - 4*det*det))) / 2));
              return {text: n.textContent, size_pt: parseFloat(s.fontSize) * scale * 72 / 96};
            });
            font_check.minimum_pt = sizes.length ? Math.min(...sizes.map(s => s.size_pt)) : null;
            font_check.small_text = sizes.filter(s => s.size_pt + 0.01 < minFontPt);
            font_check.status = !sizes.length ? 'NOT AUDITABLE' : font_check.small_text.length ? 'REVIEW REQUIRED' : 'PASS';
          }
          return {canvas_overflow, text_collisions, font_check};
        }, {widthMm, minFontPt}));
        await page.pdf({path: stem + '.pdf', printBackground: true, preferCSSPageSize: true});
        report.blocked_requests = blocked;
        const hardFailure = report.canvas_overflow.length || blocked.length;
        const needsReview = report.text_collisions.length || ['REVIEW REQUIRED', 'NOT AUDITABLE'].includes(report.font_check.status);
        report.status = hardFailure ? 'FIX BEFORE DELIVERY' : needsReview ? 'REVIEW REQUIRED' :
          widthMm === undefined ? 'PREVIEW ONLY' : 'AUTOMATED CHECKS PASSED';
        if (hardFailure || (strict && needsReview)) failed = true;
      } catch (error) {
        report.error = error.message;
        report.status = 'FIX BEFORE DELIVERY';
        failed = true;
      } finally {
        report.blocked_requests = blocked;
        fs.writeFileSync(stem + '.render-check.json', JSON.stringify(report, null, 2) + '\n');
        await page.close();
      }
      console.log(`${path.basename(file)}: ${report.error || report.status}`);
    }
    await context.close();
  } finally {
    await browser.close();
  }
  if (failed) process.exitCode = 1;
}

main().catch(error => {console.error(error.message); process.exitCode = 1;});
