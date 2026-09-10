# Evidence-led layout demonstration

**All counts are invented for testing and layout demonstration. They are not
results from any research project.** Rebuild with
`python scripts/make_evidence_example.py --out examples/evidence-design.svg`.

## Design brief

Question: how can an aggregate difference be shown together with its control
logic and a conclusion-changing subgroup? Panel a carries aggregate evidence;
panel b explains what is held fixed; panel c bounds the aggregate pattern.
The larger top panel and smaller lower panels are intentional, not an equal-grid
template. Intended demonstration width: 180 mm; reflow before single-column use.

## Caption

**Illustrative selection comparison.** a, Synthetic correct-selection counts
for two selectors across five equal-sized cohorts. Both bars start at zero and
use the same denominator. b, Hypothetical matched design holding cases,
candidate pools and reference labels fixed while changing the selector.
c, Cohort-level differences in correct counts (B minus A), including the
negative difference in cohort E. No confidence intervals or significance tests
are implied; aggregate counts do not supply paired case-level outcomes.

## Source/data manifest

Source: the `COHORTS` constant in `scripts/make_evidence_example.py`.
Unit: illustrative case. Each cohort contains 50 cases; total denominator 250.
Missing/failed cases: none in this artificial fixture. No real images or data.

| Cohort | Selector A correct | Selector B correct | B minus A |
|---|---:|---:|---:|
| A | 28 | 36 | +8 |
| B | 31 | 37 | +6 |
| C | 35 | 39 | +4 |
| D | 38 | 40 | +2 |
| E | 39 | 38 | -1 |
| Total | 171 | 190 | +19 |

The caption and this manifest belong outside the artwork. Only necessary
labels and the synthetic-data disclosure appear inside it.
