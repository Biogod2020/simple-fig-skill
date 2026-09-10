# Evidence-first publication design

Adapted and substantially rewritten from the `nature-figure` design and
multi-panel guidance in Yuan1z0825/nature-skills (Apache-2.0). Changes: condensed
into an SVG-first workflow; retained Simple Fig's titles and palette; removed
backend gates and rigid panel rules; corrected blanket axis/normalization advice.
See [source attribution](../THIRD_PARTY_NOTICES.md) and the included license.
These are editorial heuristics, not Nature's official requirements.

## 1. Decide what the figure must establish

Before a substantial redesign, write a few lines:

```text
Question and supported claim:
Strongest alternative explanation / result that could overturn it:
Sources, unit of analysis, denominator, missing cases:
Panel -> evidence role -> necessary comparison:
Decisive panel and reading order:
Final width and output formats:
```

Select the smallest sufficient set of roles: setup, primary evidence, credible
control, representative instance, decomposition, independent validation, or
failure boundary. Several metrics can test one claim, but metric diversity
alone does not justify more panels. Remove a panel mentally: what inference
would disappear? Repetition belongs in a shared axis, supplement or nowhere.
Never demote a negative result that materially changes the claim.

A useful reading sequence is **establish -> compare/control -> qualify**.
Use only the steps the evidence needs. A method diagram is not a default opening
panel, nor does every figure need an ablation or a representative image.

## 2. Match composition to evidence

| Archetype | Useful structure | Avoid |
|---|---|---|
| Decisive-result-led | Large primary comparison plus quieter control and boundary views | Equal-sized tiles that give secondary metrics equal authority |
| Mechanism-led | Readable central mechanism with one measured discriminator | A large flowchart with no evidence for its mechanism |
| Image plus measurement | Matched real images plus population-level quantification | Attractive examples that imply an unmeasured population effect |
| Population to instance | Distribution/map, quantified relation, informative real case | An anecdote disconnected from the aggregate |

Use shared grid boundaries, a small set of gutters and common panel-title
baselines. Comparable plots should have comparable **plot areas**, not just
equal outer canvases. Check the final rendered left/right edges, axis baselines,
widths, heights and gutters. Allocate explicit comparable groups when a hero
panel spans cells; do not force every panel to match the hero's dimensions.
Colorbars, insets and intentionally different-width panels need documented
layout decisions, not a looser global tolerance.

Use whitespace and alignment instead of rounded-card grids. Keep one short
panel title, and move interpretation to the caption. Directly label short,
spatially stable series; otherwise use one quiet shared legend. Never reserve
an entire extra panel for a legend automatically.

## 3. Coordinate color families without distorting the science

Default to the existing [Simple Fig palette](style-guide.md). A small number
of semantic families should connect all panels: the same method, tissue class,
condition or intervention keeps the same mapping. Distinguish categorical
identity, ordered model variants and signed effects; they are different encodings.

For a softer comparison figure, this optional family recipe is adapted from
upstream's pastel example; it is not a journal-specific mandatory palette:

| Family | Swatches | Use |
|---|---|---|
| Cool comparators | `#484878`, `#7884B4`, `#B4C0E4` | Related comparators; add markers or direct labels |
| Lilac/rose focal variants | `#E4E4F0`, `#E4CCD8`, `#F0C0CC` | Light fills with dark ink text and visible outlines |
| Neutral scaffolding | Existing ink, muted and light tokens | Axes, reference marks, quiet separators |

Light swatches are not suitable as small text or thin lines on white. For
ordered variants, use ordering plus labels/markers rather than relying on
subtle hue differences. Check grayscale and color-vision-deficiency views;
neither this palette nor an automated text-box pass proves accessibility.
Do not make a scientifically important baseline unreadably pale to flatter
the focal method. Do not assign red to a comparator merely because it lost.
For genuine signed effects, use a meaningful center and a redundant sign/shape.

Preserve image channels, categorical masks and quantitative color mappings.
Do not recolor them for branding. Avoid rainbow scales, gratuitous gradients,
shadows and 3D geometry unless the extra visual dimension encodes real data.

## 4. Design at the final physical width

Keep the existing sans-serif family and verify an available font. As an
editorial starting point, use roughly 8–10 pt body labels, a slightly larger
panel heading, and strokes around 0.5–1 pt at final size. Dense figures may
need different values. These are not universal submission rules.

```text
final_font_pt = svg_font_units * width_mm * 72 / (25.4 * viewBox_width)
svg_font_units = desired_font_pt * 25.4 * viewBox_width / (72 * width_mm)
```

At 180 mm wide with a 1400-unit viewBox, 26 units are about 9.48 pt; at 89 mm,
they are only about 4.69 pt. An unchanged double-column design does not become
a readable single-column design just by shrinking it. Reflow or simplify it.
Check small annotations, scale bars and superscripts as well as main labels.
Widths in examples are chosen demonstration sizes, not prescribed by Nature.

## 5. Choose an honest quantitative encoding

| Question | Prefer | Integrity check |
|---|---|---|
| Compare estimates with uncertainty | Aligned dots/intervals or a forest plot | Define SD, SEM or CI; preserve the independent sampling unit |
| Compare counts or magnitudes | Directly labeled zero-based bars | Same denominator; do not truncate ordinary bars to amplify a gain |
| Inspect paired changes | Paired dots/lines or a signed change plot | Match actual units; disclose exclusions; do not imply pairing from totals |
| Show distributions | Raw points with appropriate distribution summaries | Show n; a violin can imply too much structure with very few observations |
| Show temporal behavior | Lines with consistent uncertainty and reference | Keep shared scales; do not connect missing observations silently |
| Show a matrix | Sequential scale for magnitude; diverging scale for signed deviations | Share normalization across comparable values; label any local normalization |
| Show real images | Aligned fields/conditions plus honest scale bars | Match crop, aspect ratio and preprocessing; document selection |

A focused nonzero range can be appropriate for points or line trends when it
is explicitly labeled. Do not transfer that convention blindly to bar lengths.
Do not infer causal attribution from an architecture cartoon, significance
from aggregate counts, or independent replication from correlated cells,
patches or repeated measurements. Missingness is not the same as zero. Prefer
small multiples to radar charts when axis normalization or area would mislead.
Do not manufacture uncertainty, statistics or measurements to complete a layout.

## 6. Final review

Read the figure at intended paper width, not only at large browser zoom.
Confirm that the decisive evidence is clear, necessary controls are visible,
each panel adds an inference, and the caption agrees with the source data.
Review rendered text/mark collisions, panel alignment, legend spacing, scale
bars and meaningful color differences. Inspect the PDF too.

The bundled renderer checks canvas overflow, candidate text/text collisions
and optional final-width text size. It does **not** automatically audit panel
alignment, text/data collisions, font identity or statistical validity.
Record any unchecked items and explanations for intentional overlaps; rerun
after edits. See [export-and-check.md](export-and-check.md).
