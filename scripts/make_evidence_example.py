"""Original evidence-layout demo. ALL counts are synthetic, not research results."""

import argparse
from pathlib import Path

from svg_figure import COLORS as C, SvgFigure

# Five equally sized, invented cohorts. Do not infer paired significance from totals.
COHORTS = [('A', 28, 36), ('B', 31, 37), ('C', 35, 39), ('D', 38, 40), ('E', 39, 38)]
PER_COHORT = 50


def build(destination: Path) -> None:
    f = SvgFigure(1400, 880, 'Illustrative counts only; not experimental data. Aggregate evidence, matched design, and a negative subgroup.')
    f.panel(40, 55, 'a', 'Aggregate selection')
    f.text(40, 108, 'Synthetic example: 5 cohorts, 50 cases each', 26, C['muted'])
    total = PER_COHORT * len(COHORTS)
    x0, unit = 265, 3.7
    for y, label, index, color in [(175, 'Selector A', 1, C['gray']), (272, 'Selector B', 2, C['blue'])]:
        n = sum(row[index] for row in COHORTS)
        f.text(40, y + 32, label, 29)
        f.rect(x0, y, n * unit, 46, color, color, 0)
        f.text(x0 + n * unit + 22, y + 32, f'{n}/{total} ({n/total:.1%})', 27, weight=600)
    f.path(f'M{x0} 348H{x0 + total * unit}', C['muted'], 1.5)
    for value in range(0, total + 1, 50):
        x = x0 + value * unit
        f.path(f'M{x} 348V356', C['muted'], 1.5)
        f.text(x, 390, value, 26, C['muted'], anchor='middle')
    f.text(1320, 390, 'Correct', 26, C['muted'], anchor='end')

    f.panel(40, 488, 'b', 'Matched design')
    f.rect(40, 578, 222, 128, 'white', C['light'], 4)
    f.text(151, 616, 'Same cases', 28, anchor='middle')
    f.text(151, 652, 'Fixed candidates', 26, C['muted'], anchor='middle')
    f.text(151, 688, 'Fixed reference', 26, C['muted'], anchor='middle')
    f.path('M280 644H313V604H344', C['muted'], 2)
    f.path('M313 644V712H344', C['muted'], 2)
    f.arrow(332, 604, 370)
    f.arrow(332, 712, 370)
    for y, label, color in [(570, 'Selector A', C['muted']), (678, 'Selector B', C['blue'])]:
        f.rect(385, y, 197, 68, 'white', color, 4)
        f.text(483.5, y + 44, label, 28, color, anchor='middle')

    f.panel(690, 488, 'c', 'Cohort boundary')
    f.text(690, 542, 'Change in correct selections (B minus A)', 26, C['muted'])
    origin, step = 900, 37
    f.path(f'M{origin} 571V793', C['light'], 2)
    for i, (name, a, b) in enumerate(COHORTS):
        y, delta = 592 + i * 46, b - a
        color = C['blue'] if delta >= 0 else C['orange']
        f.text(725, y + 8, name, 27)
        end = origin + delta * step
        f.path(f'M{origin} {y}H{end}', color, 3)
        f.circle(end, y, 6, color)
        f.text(end + (19 if delta >= 0 else -19), y + 8, f'{delta:+d}', 27,
               color, anchor='start' if delta >= 0 else 'end')
    for value in [-2, 0, 4, 8]:
        f.text(origin + value * step, 844, value, 26, C['muted'], anchor='middle')
    f.write(destination)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    build(args.out)
    print(args.out)
