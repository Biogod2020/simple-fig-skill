# Visual grammar

Use this as a starting style, adapting proportions to the actual evidence.

## Typography and hierarchy

One bold panel letter followed by one short regular or semibold title. Usually
use a 2–5-word noun phrase; do not trade away scientific precision just to
satisfy a word count. No visible overall banner, secondary subtitle, or
explanatory paragraph inside the figure. A caption outside the artwork may
explain the scientific claim, definitions and limitations.

Use a portable sans-serif family consistently (for example Arial/Helvetica or
a verified installed substitute such as Nimbus Sans). Verify the actual font
used by the renderer. Default ordinary text to pure black `#000000`: titles,
axes, ticks, legends, scale labels and local annotations. Use ordinary body
weight and modest size differences; keep bold for panel letters and occasional
short titles rather than every number, gene or result. Avoid decorative display
fonts and branding-style colored/bold headings.

When the author requests all-black text, use a small white label backing on a
dark tissue image so the label stays readable. A scale-bar stroke can remain
white for contrast; it is a graphical mark, not lettering. Preserve its length
and image calibration. Otherwise, an established dark-ink style or a justified
high-contrast label can be retained when the current task calls for it.
“No subtitle” does not remove brief action/object labels needed to read a
workflow. Keep them next to their object rather than in a full-width row.

For a 1400 × 850 SVG, start with:

| Token | Starting value |
|---|---:|
| Panel letter | 33 units, bold |
| Panel title | 31 units, semibold |
| Main node / data label | 27–30 units |
| Minor necessary label | 26 units |
| Outer margin | 40 units |
| Panel gap | 40–65 units |
| Main stroke | 2–2.5 units |
| Separator / grid | 1 unit |
| Corner radius | 4–8 units |

These are scalable design tokens, not fixed pixel or venue requirements.
At 5.5 inches / 396 PDF points wide, 26 SVG units become 7.35 pt and 31
become 8.77 pt: `label_units × width_inches × 72 / viewBox_width`.
For a different final width, compute again. Inspect at final size and enlarge
labels or simplify the panel if needed; do not rely on zoomed previews.

## Palette

| Role | Color | Use |
|---|---|---|
| Ink | `#000000` | Ordinary text, titles and axes |
| Muted | `#697586` | Neutral graphical marks; ordinary text still uses ink |
| Blue | `#3164AD` | Primary method / evidence |
| Purple | `#7962AB` | Transformation / generation |
| Teal | `#21877B` | Checks or a distinct class |
| Orange | `#BF642F` | Human action or an exception |
| Gray | `#98A3B1` | Comparator marks; use darker text |
| Light | `#DCE2E9` | Dividers and subtle outlines |
| Background | `#FFFFFF` | Canvas |

Assign a color a consistent meaning within each figure. Method colors and
class colors need not be identical, but their legends must be unambiguous.
Use text, position or shape as well as color. On gray fills, prefer ink labels
over white; verify contrast rather than assuming every palette pair works.
Changing text to black does not desaturate scientific images, expression maps,
cell boundaries, curves or heatmaps. Preserve those meaningful encodings.

## Layout recipes

- **Method:** one readable left-to-right flow; secondary panels can expand a
  checks/repair loop and a final human decision. Grouping brackets identify
  scope; group labels are concise and never compete with panel titles. Preserve
  actual step numbering—evidence preparation need not become another step.
- **Results:** give most space to a comparable-scale quantitative view. Use
  direct counts or numerator/denominator labels where informative. Pair with
  a mechanism, changed-case view, or failure composition only if measured.
  Unit dots are useful for small integer counts; say what one dot represents.
- **Image plus evidence:** retain real image geometry, align image frames,
  and pair with a compact result or review-status view. If source viewports
  differ, do not present them as a matched field without checking provenance.

Avoid 3D boxes unless the third dimension means something, gradients, shadows,
thick decorative borders, giant numerals used as marketing claims, terminal
walls and large status badges. A quantitative heatmap's continuous color scale
is a data encoding, not a forbidden decorative gradient.

Use purposeful icons as diagram objects: a magnifier for inspection, a document
for source evidence, or a restrained robot for an agent. Prefer a consistent
editable SVG family over platform-dependent emoji. If robots are requested,
connect them to inputs, operations and feedback; a repeated robot can denote
successive actions of the same agent and must not imply extra agents. A small
smile is compatible with a professional outline icon. Avoid toy mascots,
hand-drawn jitter, distressed textures and deliberate alignment errors.

For concrete workflows, visual density and reference-matched icons, see
[agent-method-figures.md](agent-method-figures.md). The author's resolved
preferences and earlier alternatives are in [session-lessons.md](session-lessons.md).

## Quantitative choices

Bar baselines usually start at zero. Disclose any justified axis truncation.
Use the same scale for comparisons; include units and the independent unit.
Stacked class counts describe composition, not accuracy. Do not let a selected
cohort imply global recall. Show failures and missingness in the denominator or
caption. Use uncertainty only when its estimand and computation are supported.
Do not add stars or error bars just because a conference figure often has them.

For dense method comparisons, see [quantitative-comparisons.md](quantitative-comparisons.md)
for grouped bars with observations, compact effect plots and significant-only
annotation with complete statistical reporting outside the artwork.
