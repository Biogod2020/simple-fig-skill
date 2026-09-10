---
name: simple-fig-skill
description: Create or restyle scientific paper figures with restrained ML-paper and Nature-inspired evidence design, short panel titles, editable SVGs, final-size PDF checks, and optional LaTeX previews. Use for method diagrams, benchmark comparisons, multi-panel results, and image-plus-result panels, especially when adapting existing scientific assets.
---

# Simple Fig

Make the evidence easy to read. Use flat vector geometry, a white background,
short labels, restrained semantic color, and a clear panel hierarchy. This is
an editorial style, not an official ICLR or Nature template or a guarantee of
submission compliance.

## Design decisions

- Give each figure one scientific question. Each lettered panel has exactly
  one short title immediately after `a`, `b`, `c`, etc. Do not add a visible
  figure-wide banner, a second panel subtitle, status badges, or prose footers
  inside the artwork. Keep axes, legends, process labels and necessary data
  annotations; these are not extra titles. Put explanations in the caption.
- Preserve useful source images and recognizable scientific concepts, while
  adapting layout to the current finding. Neither a wholesale redesign nor
  copying every old panel is the default. Move obsolete or weakly related
  resource statistics out of the main figure when they distract from its claim.
- Prefer evidence and mechanisms over decorative architecture: a compact
  workflow, a directly labeled comparison, and a real example usually carry
  more information than many rounded cards, icons, or implementation names.
- Start with 2–4 panels when useful, but choose count and proportions from the
  content. Give the decisive result or real image the principal visual area.
  Do not force every task into a three-panel template. A schematic is not
  automatically panel a; distinguish setup, effect, control and failure boundary.
- Use the palette and spacing in [style-guide.md](references/style-guide.md)
  when creating a new design. Preserve existing semantic palettes for masks,
  quantitative heatmaps, and other encoded scientific data.

## Plan only what the task needs

For a new or substantially rearranged multi-panel figure, read
[evidence-design.md](references/evidence-design.md). Record a compact brief:
question, supported claim, evidence that could overturn it, source/denominator,
each panel's inferential role, and intended physical width. This may be a short
note beside the source, not a mandatory separate planning document. A small
label edit should not trigger a new figure-planning ceremony.

Reuse the task's existing Python, R or SVG workflow. For a new simple diagram,
use native SVG; for statistical plots use a suitable available plotting tool.
Do not interrupt routine work with a compulsory backend question, persist new
global preferences, or install another skill. Load references only as needed.

## Work from evidence

Read the user's supplied figures and the exact result artifacts relevant to
the intended claim. Separate reusable scientific material from obsolete labels
or purely decorative elements. Establish the unit, denominator, cohort/run,
reference-label definition, and missing/failed cases before plotting numbers.

Keep prediction composition, technical execution, scientific correctness,
human review status, and measured reviewer efficiency distinct. For example,
“reviewed without a flag” is not automatically “independently validated,” and
an operational failure is not necessarily a scientific negative. These are
examples of distinctions to preserve, not mandatory panels for every paper.

Plot measured results from source data. Do not invent gains, sample sizes,
uncertainty, significance, timing curves, or favorable outcomes to fill a
layout. In a planning preview, a pending study may be shown as a clearly marked
experimental design without simulated results; move or replace it for a final
results figure. The bundled demo numbers are explicitly illustrative and must
never be reused as research evidence. Preserve conclusion-changing negative
results; visual emphasis must not conceal a strong comparator or a failure.

## Draw and refine

1. Choose one short title and visual encoding per panel. Remove a panel only
   when it adds no necessary inference; a second metric is not automatically a
   second scientific argument. Put caveats in the caption unless essential to
   interpreting a mark. Match panel order to the evidence, not to a stock grid.
2. Reuse appropriate images without changing their geometry, scale bars,
   coordinate alignment, or encoded colors. Keep originals intact; edit copies.
   Rebind legacy examples to the final source/run before making new claims.
3. Draw editable vectors. Use the existing plotting environment for complex
   statistical plots; use native SVG for diagrams and simple comparisons.
   The [SVG helper](scripts/svg_figure.py), [original example](scripts/make_example.py)
   and [evidence-layout example](scripts/make_evidence_example.py) are optional
   starting points, not mandatory templates.
4. Render, inspect, and fix the actual output. Check text clipping, text/mark
   collisions, plot-area alignment, legend contrast, shared encodings, comparable
   scales, and caption correspondence. Preserve zero baselines for ordinary
   magnitude bars; use a point/interval plot when a focused range is needed.
   Prefer reducing content or rearranging panels to shrinking typography.
5. Export requested SVG/PDF/PNG artifacts and, when requested, a LaTeX preview.
   For final-width SVG-to-PDF export, use `--width-mm` and examine the check
   record. Repeat QA after changes. Report what was checked and distinguish a
   layout preview from a final submission-ready figure. Do not publish, install
   globally, or change experiments unless that action is within the request.

Read [export-and-check.md](references/export-and-check.md) when rendering,
compiling LaTeX, or evaluating final-size legibility. Automated pass means only
that the implemented checks passed, not that all collisions, font substitutions,
panel alignment or scientific errors have been excluded. Verify the target
venue's current instructions when actual compliance is requested.

## Deliverables

Honor the requested formats. A usual package contains the editable SVG,
rendered PDF/PNG, a short caption, and the small source/data manifest necessary
to reproduce the figure. Include final width, completed checks and unresolved
warnings in the validation note. Add LaTeX source only when useful or requested.
Preserve the user's language and established terminology. Keep the final
message short and link to the preview and editable source.
