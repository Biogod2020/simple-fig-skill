# Quantitative comparisons that read like a paper

Use this guide when a benchmark figure feels sparse, monotonous or difficult
to compare. The goal is more readable evidence per unit of space, not more
decoration. These are adaptable design choices, not a fixed journal template.

## Choose familiar plots from the comparison

| Evidence question | Useful starting point | What must remain visible |
|---|---|---|
| Before/after across a few categories | Narrow grouped bars with observed unit-level points; paired dots/lines when individual changes matter | Zero baseline for bars, the observation unit and actual pairing |
| Several methods across datasets | Grouped bars or aligned dot plots, with a fixed method order | Every required dataset and comparator, common scales and aggregation weights |
| Improvement relative to a reference | Compact horizontal point-and-interval plot | Signed difference, full intervals, zero reference and direction of benefit |
| Distribution across many units | Raw points with a justified box or distribution summary | Sample size, spread and the independent sampling unit |

A bar with observation points can communicate both the headline estimate and
heterogeneity. Use small open markers with dark outlines when they remain
legible over the fills. Apply deterministic horizontal offsets only; never
jitter the measured score. Keep model pairing recoverable in source data and
show it graphically when pairing is the central question. With one or two
observations, show those observations directly rather than fitting a violin
density. A single source mean is not a replicated experiment.

Do not impose bars on every task. Use dots/intervals when differences or
uncertainty are the main evidence, and horizontal layouts when long labels
need them. Heatmaps suit larger matrices; radar area and decorative ranking
cards usually make precise method comparisons harder.

Reducing tables does not mean removing meaningful matrices or using dots
everywhere. A confusion matrix or platform-by-species heatmap encodes a real
two-dimensional relation. A source-icon column plus a compact percentage
matrix can make evidence types easier to recognize; define row/column
denominators. Put long lookup tables of exact scores in a formal table or
supplement. Pies/donuts are optional for a small number of mutually exclusive
parts of one whole, especially when requested; overlapping coverage measures
cannot be added into a whole. Do not give every panel the same plot type just
for visual uniformity.

## Add information without adding clutter

An image-plus-benchmark figure can read as **visible change -> breadth of
improvement -> external comparison**. A compact effect plot can qualify the
last comparison when uncertainty matters. This is one useful sequence, not
a requirement for four panels or external validation in every figure.

- Allocate height from the user's priorities and final print size. If the
  image gallery is capped at two-fifths of the height, design within that cap;
  do not generalize that proportion to every paper.
- Two related metrics can share a lettered panel as aligned coordinate areas.
  Label each metric on its axis, avoiding repeated headings and explanations.
- Give secondary comparisons only the height needed for readable marks and
  labels. Align plot areas and title baselines; equal outer boxes are not
  sufficient. Break long category names onto short lines before rotating them.
- Use one quiet shared legend with identical left-to-right method order.
  When a panel contains only a subset, preserve its relative order and state
  the subset. Keep each method's color consistent across panels.
- Separate a macro-average group from individual datasets with a small gap
  or a thin divider. Explain its weighting in the caption. An image-weighted
  mean, dataset macro-average and pooled-instance metric are not interchangeable.
- Keep an effect plot to reference labels, points, intervals and a zero line.
  Put exact values in source data or the caption unless numerical labels add
  something the axis cannot. Avoid a second numeric table beside the same marks.

For a conventional results style, start with a white canvas, thin dark axes,
restrained solid fills and small black-edged points. Remove top/right spines
or grids when they add no reading aid. Give observations at the maximum score
enough headroom to avoid clipping. Use a distinguishable neutral baseline and
one clear focal color; do not make comparators unreadably pale. Position,
labels or marker shapes should support identification beyond hue alone.

When learning from published figures, inspect the actual relevant panels or
authors' plotting code. Match the visual grammar to the number of groups and
the observation level in the current data. Record which design choice was
borrowed; do not transplant their error bars, tests or significance stars.
An approved design or a small label edit does not require a new literature search.

## Make significance precise and quiet

For dense main figures, prefer annotating only meaningful planned comparisons
that meet the stated statistical threshold, unless the user or reporting
requirements call for all labels or exact p values. Omit `ns` from the artwork
in the significant-only style. This is a display policy, not a result filter:
retain the compared marks, uncertainty and every tested contrast in the
caption or accompanying source table. State the display policy in the caption.

- Read the existing analysis plan and results first. A styling request does
  not authorize selecting a different metric, test family or threshold to
  obtain stars. If valid tests are absent, do not infer them from bar heights
  or CI overlap; treat the statistical analysis as a distinct, scoped task.
- Map annotations to the actual reported p values, including the specified
  multiple-comparison correction. Define the symbols, threshold, test,
  independent unit, pairing and correction family outside the artwork.
- Place brackets or labels only over the contrasts they test. If the test is
  an overall weighted effect across categories, use an explicit label such
  as `Overall *` in clear space above that metric. Do not put a star over each
  category or imply category-specific significance from the overall test.
- Small repeated fields, cells, slices or inference seeds do not automatically
  become independent replicates. Respect patient, source or dataset blocks
  and the original aggregation weights; the displayed dot and inferential
  unit may differ, so explain both.
- Keep effect sizes and uncertainty available. Statistical significance is
  not effect magnitude or practical importance. Nonsignificance does not
  establish equivalence or noninferiority; those require an appropriate design
  and a justified margin, not a visual convention.

Prefer a small number of well-scoped annotations to a forest of brackets.
Reserve annotation space in the layout rather than shrinking the data area
or letting stars collide with titles, legends or observations.

## Emphasize a supported advantage

Use consistent ordering, clear color and an appropriate paired comparison to
make an advantage easy to see. Preserve the evaluated cohort, label budget,
methods, denominators and scoring definitions. Do not drop difficult datasets,
hide a strong comparator or change aggregation because the ranking is inconvenient.
If reasonable aggregates differ, identify the plotted estimand and preserve
the alternative result where it affects interpretation.

Keep example selection separate from quantitative coverage. When the user
asks for high-improvement images, document the selection criterion and label
them as selected illustrations; do not call them typical or let them replace
the complete-cohort comparison. Match the image, reference and prediction
geometry, run and preprocessing before interpreting any visible gain.

A compact ROC may share a panel with the failure case it quantifies. Keep the
case legible and the axes/legend readable; do not replace the case merely to
fit a new metric. Identify the dataset, error construction, evaluated scorer
version and subset in the caption. A favorable large-misalignment subset does
not establish all-error or current-system performance. If such a subset is
selected after inspection, disclose that choice and retain the full evaluation
and conclusion-changing failures in the supplement. AUROC, average precision,
thresholded sensitivity and precision are distinct quantities. Investigating
an unexpectedly low AUC starts with versions, rows, labels, score direction and
aggregation, not selection of a better-looking result.

## Revise an approved figure without restarting it

For a request such as "remove ns," preserve the approved data, crops, colors,
axes and proportions. Reuse valid computed results and alter only the intended
annotation layer. Do not rerun training, inference or an unchanged statistical
analysis just to redraw text.

Inspect the newly exported PDF at the intended physical width, including
annotation collisions and caption correspondence. Where useful, compare
unchanged regions against the approved render; pixel equality is informative
only under the same rasterization settings. Reuse prior checks for unchanged
data and geometry, and repeat checks affected by the edit. A textual source
change alone does not prove that the delivered PDF changed correctly.

Keep editable source, rendered output, captions and the compact result table
together. A plot with two displayed stars can still have five fully reported
tests. Preserve previous versions so that visual refinement remains traceable.
