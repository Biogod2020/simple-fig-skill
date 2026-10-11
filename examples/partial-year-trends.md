# Partial-year trend example

[Editable SVG](partial-year-trends.svg) · [Synthetic counts and denominators](partial-year-trends.data.json) · [Source](../scripts/make_partial_year_example.py)

All counts are invented to demonstrate presentation. They are not GEO statistics
or biological results. The two modalities need not be mutually exclusive.

Complete-year curves end at 2025. Separate open points show 2026 year-to-date
shares through 9 October, each divided by the eligible records in that same
partial period. Both partial-year points are lower than the preceding complete
year; their values remain visible, with no connecting segment or implied
full-year endpoint. The diagram does not establish why those values differ or
predict how the year will finish.

Independent percentage axes show each category's own trajectory; their visual
slopes do not compare growth rates across categories. Plain black labels remain
readable while the data curves keep distinct colors.

```bash
python scripts/make_partial_year_example.py --out examples/partial-year-trends.svg
node scripts/render_svg.cjs examples/partial-year-trends.svg \
  --width-mm 180 --min-font-pt 7 --strict
```

The generator also writes the `.data.json` ledger. For a scientific result,
replace this synthetic source with a registered input and a defined period;
choose common calendar windows if annual changes are the actual question.
