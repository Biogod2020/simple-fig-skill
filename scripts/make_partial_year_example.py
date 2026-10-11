"""Editable partial-year demonstration; all counts are synthetic, not research results."""

import argparse
import json
from pathlib import Path

from svg_figure import COLORS as C, SvgFigure


# Invented counts illustrate period handling, not a biological trend.
YEARS = list(range(2018, 2026))
ANNUAL_TOTALS = [250] * len(YEARS)
SERIES = [
    ('Bulk RNA', [208, 197, 180, 170, 160, 155, 145, 135], 25, 100, C['purple']),
    ('Spatial sequencing', [1, 1, 2, 3, 5, 7, 10, 13], 2, 6, C['teal']),
]
YTD_TOTAL = 60
CUTOFF = '2026-10-09'


def build(destination: Path) -> None:
    """Separate YTD points while preserving their own observed-period denominator."""
    f = SvgFigure(1400, 830, 'Synthetic counts only; not research results. Complete-year curves and separate year-to-date shares.')
    x0, xlast, xytd = 115, 970, 1150
    ledger = []
    for i, (title, counts, ytd_count, maximum, color) in enumerate(SERIES):
        shift = i * 390
        top, bottom = shift + 140, shift + 310
        f.panel(40, shift + 55, chr(ord('a') + i), title)
        f.text(40, shift + 101, 'Synthetic annual share (%)', 26)
        f.text(1080, shift + 74, '2026 YTD', 26)
        f.text(1080, shift + 110, 'through 9 Oct', 26)
        f.path(f'M1040 {shift + 128}V{shift + 370}', C['light'], 1.5)
        x = lambda year: x0 + (year - YEARS[0]) / (YEARS[-1] - YEARS[0]) * (xlast - x0)
        y = lambda value: bottom - value / maximum * (bottom - top)
        for tick in [0, maximum / 2, maximum]:
            f.path(f'M{x0} {y(tick)}H{xlast}', C['light'], 1)
            f.text(x0 - 17, y(tick) + 9, f'{tick:g}', 26, anchor='end')
        points = [(year, 100 * count / total) for year, count, total in zip(YEARS, counts, ANNUAL_TOTALS)]
        curve = 'M' + ' L'.join(f'{x(year):.3f} {y(share):.3f}' for year, share in points)
        f.path(curve, color, 3)
        f.circle(x(YEARS[-1]), y(points[-1][1]), 5, color)
        ytd_share = 100 * ytd_count / YTD_TOTAL
        # A separate open circle is not connected to the last complete year.
        f.path(f'M{xytd - 6} {y(ytd_share)} a6 6 0 1 0 12 0 a6 6 0 1 0 -12 0', color, 2.5, C['white'])
        f.text(xytd + 22, y(ytd_share) + 9, f'{ytd_share:.1f}%', 27)
        for year in [2018, 2020, 2022, 2025]:
            f.path(f'M{x(year)} {bottom}V{bottom + 8}', C['ink'], 1)
            f.text(x(year), bottom + 42, year, 26, anchor='middle')
        for year, count, total, (_, share) in zip(YEARS, counts, ANNUAL_TOTALS, points):
            ledger.append({'modality': title, 'year': year, 'count': count, 'eligible_records': total,
                           'share_pct': share, 'period': 'complete year', 'display': 'annual curve'})
        ledger.append({'modality': title, 'year': 2026, 'count': ytd_count, 'eligible_records': YTD_TOTAL,
                       'share_pct': ytd_share, 'period': 'year to date', 'cutoff': CUTOFF,
                       'display': 'separate open point'})
    f.write(destination)
    destination.with_suffix('.data.json').write_text(json.dumps({
        'data_status': 'synthetic; not research results',
        'independent_y_axes': True, 'rows': ledger,
    }, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    build(args.out)
    print(args.out)
