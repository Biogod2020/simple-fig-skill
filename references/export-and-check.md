# Build, export and inspect

## Optional tools

`scripts/svg_figure.py` uses only Python 3.10+ and its standard library. It creates
escaped SVG text, panel headings, shapes, inline raster assets and descriptions.
For complex statistical plots, reuse the project's existing Python/R tools and
preserve editable vector export where feasible.

```bash
python scripts/make_example.py --out build/example.svg
node scripts/render_svg.cjs build/example.svg

# Evidence-led design demo; every count is synthetic.
python scripts/make_evidence_example.py --out build/evidence-design.svg
node scripts/render_svg.cjs build/evidence-design.svg \
  --width-mm 180 --min-font-pt 7 --strict
```

The renderer needs Node.js, Playwright and Chromium. Reuse an available
environment first. `PLAYWRIGHT_MODULE` may name an installed module or absolute
module directory; `CHROMIUM_PATH` may specify an existing browser. Otherwise
normal `require('playwright')` resolution and its configured browser are used.
When dependency installation is appropriate, use a task-local environment;
nothing is installed or updated automatically. `CHROMIUM_NO_SANDBOX=1` is an
explicit opt-in for environments that need that flag; the default retains the
browser sandbox. No plotting backend, external API or new dependency is required
by the added checks.

Inputs must be static, self-contained SVGs with a positive numeric `viewBox`.
Inline raster images as data URIs (`SvgFigure.image` does this). External
requests are blocked and reported. Scripts, event handlers and foreignObject
are rejected. This is not a general-purpose sanitizer for hostile SVGs.

Outputs are sibling `.png`, `.pdf` and `.render-check.json` files, or go to
`--out-dir DIRECTORY`. They are overwritten on rerun. Batch output-name
collisions are rejected. A failed run can leave diagnostic or previous output
files; use the exit status and the latest JSON, not file existence, to decide
whether a render succeeded.

## Physical size and automated checks

Without `--width-mm`, the original viewBox-sized preview behavior is retained.
It is a layout proof, **not** a final-size typography audit. Root SVG width/height
attributes alone do not select publication size in this renderer.

With `--width-mm N`, the PDF is printed at that width and its proportional
height. The PNG remains a viewBox-resolution screen preview; it is not a
300-dpi submission raster or proof of print-only CSS. Inspect/rasterize the PDF
for those purposes. Verify the exported PDF's actual page size with `pdfinfo`
or a PDF reader; browser pagination can round physical dimensions slightly.

The JSON reports:

- `canvas_overflow`: transformed text outside the root canvas (hard failure).
- `text_collisions`: candidate overlaps between rendered text-element boxes.
  Rotated labels can produce false positives because the boxes are axis-aligned.
- `font_check`: optional final-width effective font sizes including ancestor
  transforms and tspan sizing. Default threshold: 7 pt, an editorial check,
  **not** a universal journal requirement. `--min-font-pt` requires `--width-mm`.
- `blocked_requests`, final dimensions and a limited-check status.

Checks run in print media after final sizing. A screenshot alone is not the
same artifact as that printed layout. The font check inspects CSS em size, not
every glyph outline; outlined/raster text cannot be checked and missing fonts,
font substitutions, font licensing and missing glyphs remain manual checks.
A no-editable-text document is `NOT AUDITABLE`, never a font-check pass.

Errors, external loads and canvas overflow exit nonzero. Candidate collisions,
small text and non-auditable typography produce `REVIEW REQUIRED`; `--strict`
makes them exit nonzero too. Diagnostic PDF/PNG files may still be written.
`PREVIEW ONLY` means no final width was supplied. `AUTOMATED CHECKS PASSED` means
only the implemented checks passed. Nothing automatically fixes labels, hides
results, or establishes complete publication compliance.

## Manual review and PDF verification

1. Verify sources, run/cohort, estimands, independent units, denominators,
   exclusions and whether panels are measured, legacy examples or planned.
2. Inspect every panel and the entire figure at intended width. Check text/data
   collisions, image scale bars, legend contrast, clipping, actual fonts and
   caption correspondence. Preserve scientifically meaningful color mappings.
3. Measure final comparable plot areas: shared edges, axis baselines, widths,
   heights and repeated gutters. A hero panel can intentionally span cells;
   document comparable groups and exceptions. The renderer does not do this
   alignment audit, and text-box checks do not substitute for it.
4. Inspect the actual PDF: page count, physical size, selectable text and a
   rasterized render (for example `pdftoppm`). Inspect uncertainty and overlaid
   data marks manually. For raster submission, export from the final PDF at
   the required DPI and verify embedded-image resolution separately.
5. Keep a short validation record of completed checks and unresolved warnings.
   Fix the cause and rerender after changes. Do not lower a threshold simply
   to hide unreadable text. Verify the venue's current instructions separately.

## LaTeX preview

Copy [preview.tex](../assets/preview.tex) to the render directory, update the
filenames and captions, and compile with a compatible engine:

```bash
tectonic preview.tex --keep-logs
# Or use an existing pdflatex / latexmk setup for this English template.
```

The template uses `graphicx` and `geometry`, no bundled fonts. For Chinese
captions, use a suitable XeLaTeX/fontspec/xeCJK setup with verified available
fonts. Check overfull boxes, missing glyphs and font warnings. A landscape
preview does not replace the target paper template. Scaling a checked PDF again
in LaTeX changes its effective text size; inspect that final placement too.
