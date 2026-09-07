# Build, export and inspect

## Optional tools

`scripts/svg_figure.py` uses only Python 3.10+ and its standard library. It creates escaped
SVG text, panel headings, simple shapes, inline raster assets, and a metadata
description. For complex statistical plots, use the project's existing tools
and preserve editable vector export where feasible.

```bash
python scripts/make_example.py --out /tmp/simple-fig-demo/example.svg
node scripts/render_svg.cjs /tmp/simple-fig-demo/example.svg
```

The renderer needs Node.js, Playwright and a Chromium executable. Reuse an
available environment first. `PLAYWRIGHT_MODULE` may name an installed module
or absolute module directory; `CHROMIUM_PATH` may specify an existing browser.
Otherwise the script uses normal `require('playwright')` resolution and its
configured browser. When installing dependencies is appropriate for the task,
install them in a task-local environment; this skill does not install or update
anything automatically. `CHROMIUM_NO_SANDBOX=1` is an opt-in for environments
that require that browser flag; the default keeps the browser sandbox enabled.

Inputs must be self-contained SVGs with a numeric `viewBox`. Inline local raster
images as data URIs (`SvgFigure.image` does this). The renderer blocks external
network requests and reports blocked external loads; it does not fetch remote
scientific material implicitly. It refuses destination/source name collisions
in a batch. Outputs are sibling `.png`, `.pdf`, `.render-check.json` files, or
go to `--out-dir DIRECTORY`; those generated outputs are overwritten on rerun.

Chromium prints the native inline SVG to PDF, preserving vector text and shapes.
Raster images remain raster; a PDF extension does not make them vector.

## LaTeX preview

Copy [preview.tex](../assets/preview.tex) to the render directory, update its
figure filenames and captions, then compile with a compatible LaTeX engine:

```bash
tectonic preview.tex --keep-logs
# Or use an existing pdflatex / latexmk setup for this English template.
```

The template uses ordinary `graphicx` and `geometry`, no bundled fonts. For
Chinese captions, use a suitable XeLaTeX/fontspec/xeCJK setup with verified
available fonts. Do not silently substitute missing glyphs. A landscape preview
is for design review, not a substitute for the target paper template.

## What to check

1. Verify the data manifest: run/cohort, units, denominators, definitions,
   selected subset, and whether panels are measured, legacy examples or planned.
2. Inspect every rendered page at intended paper width. Check cropped text,
   collisions, whitespace, legend contrast, arrows, panel correspondence and
   readability of image scale bars. Preserve scientifically meaningful colors.
3. For nested SVGs, `getBBox()` alone is in local coordinates. The renderer uses
   `getBoundingClientRect()` so rotated text and ancestor transforms are included.
   Its canvas-bound check does **not** establish that nested clipping, overlaps,
   tiny text, missing glyphs, or scientifically wrong diagrams are absent.
4. Inspect the actual PDF, not only the SVG screenshot. When available, use
   `pdfinfo` for page count and `pdftoppm` for page renders. Check LaTeX logs for
   overfull boxes, missing glyphs and font warnings.
5. Keep a brief validation record stating the checks actually completed and
   remaining limitations. Do not claim full venue compliance from these helpers.

The renderer exits nonzero for errors or detected canvas overflow and still
writes a check record when possible. It does not automatically modify labels,
hide failures, resize the figure, or claim that the content is scientifically
valid. Fix the cause and rerender the changed artifact.
