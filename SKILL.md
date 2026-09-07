---
name: simple-fig-skill
description: Create or restyle scientific paper figures with a restrained ML-conference aesthetic, short panel titles, editable SVGs, and optional LaTeX PDF previews. Use for method diagrams, benchmark comparisons, and image-plus-result panels, especially when adapting existing scientific assets.
---

# Simple Fig

Make the evidence easy to read. Use flat vector geometry, a white background,
short labels, restrained semantic color, and a clear panel hierarchy. This is
an editorial style suited to ML papers, not an official ICLR template or a
claim that a conference mandates one visual aesthetic.

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
  content. Make the principal result or real image visually dominant. Do not
  force every task into a three-figure or three-panel template.
- Use the palette and spacing in [style-guide.md](references/style-guide.md)
  when creating a new design. Preserve existing semantic palettes for masks,
  quantitative heatmaps, and other encoded scientific data.

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
never be reused as research evidence.

## Draw and refine

1. Choose a short title and visual encoding for each panel. Put the current
   scientific finding in the main visual position; keep methodological caveats
   in a concise caption unless a label is necessary to interpret the mark.
2. Reuse appropriate images without changing their geometry, scale bars,
   coordinate alignment, or encoded colors. Keep originals intact; edit copies.
   Rebind legacy examples to the final source/run before making new claims.
3. Draw editable vectors. Use the existing plotting environment for complex
   statistical plots; use native SVG for diagrams and simple comparisons.
   The small [SVG helper](scripts/svg_figure.py) and
   [example builder](scripts/make_example.py) are optional starting points.
4. Render, inspect, and fix the actual output. Check label clipping, spacing,
   collisions, legend contrast, comparable scales, and caption correspondence.
   Prefer reducing content or rearranging panels to shrinking the typography.
5. Export requested SVG/PDF/PNG artifacts and, when requested, a LaTeX preview.
   Report what was checked and distinguish a layout preview from a final
   submission-ready figure. Do not publish, install globally, or change
   experiments unless that action is within the user's request.

Read [export-and-check.md](references/export-and-check.md) when rendering,
compiling LaTeX, or evaluating final-size legibility. Use its deterministic
checks as aids; a no-overflow result is not a complete visual or scientific
audit. Verify the target venue's current template when actual compliance is
requested; a large landscape preview alone does not establish print legibility.

## Deliverables

Honor the requested formats. A usual package contains the editable SVG,
rendered PDF/PNG, a short caption, and the small source/data manifest necessary
to reproduce the figure. Add LaTeX source only when useful or requested.
Preserve the user's language and established terminology. Keep the final
message short and link to the preview and editable source.
