# Third-party design guidance

This update selectively adapts design guidance from
[Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills), specifically
`skills/nature-figure`. Upstream is distributed under Apache License 2.0.
A copy is provided in [licenses/nature-skills-Apache-2.0.txt](licenses/nature-skills-Apache-2.0.txt).

Reviewed revision: `7e626a86a0ac8d078be224e0a76aa1327875b0a1` (2026-09-10).
Attribution is to the nature-skills authors and contributors; no endorsement
by them or by Nature Portfolio is implied.

Relevant upstream sources:

- `skills/nature-figure/references/multipanel-evidence-architecture.md`
  (blob `c63d21905f06b22a3845d23b82c61461e6f81fd7`): distinct inferential panel
  roles, claim-driven sequencing, primary evidence and failure boundaries.
- `skills/nature-figure/references/design-theory.md`: coordinated color
  families, hierarchy, direct labels, physical-size typography and composition.
- `skills/nature-figure/SKILL.md`
  (blob `0b30d60e6aa6248ae16d62593a13a70a6adeca45`): progressive reference loading,
  rendered QA and the distinction between automated checks and human review.

## Scope and modifications

`references/evidence-design.md` is a condensed, substantially rewritten
adaptation under Apache-2.0. It carries its own modification notice. The
optional cool/lilac/rose swatches there are adapted from upstream's palette.
The rest of the update integrates those ideas through references and original
Simple Fig implementation. No upstream Python/R code, paper images, third-party
figure templates, fonts, image-generation scripts or private assets are copied.

Simple Fig retains its existing palette, short-title convention and stdlib SVG
helper. This update does not import backend-selection gates, persistent global
preferences, installation hooks, external API calls, or blanket axis-truncation
and heatmap-normalization prescriptions. New renderer checks and demo code are
independently implemented. The renderer does not claim parity with upstream's
full PDF collision or panel-alignment auditors.

This notice and the bundled third-party license apply to the identified
adaptation; they do not retroactively relicense unrelated pre-existing files.
Separately licensed materials referenced by upstream are not covered merely
because its root repository uses Apache-2.0; none are vendored here.
