"""Render a visibly labeled layout demo; the counts are not research data."""

import argparse
from pathlib import Path

from svg_figure import COLORS as C, SvgFigure


def build(destination: Path) -> None:
    f = SvgFigure(description='Style demonstration. All counts are illustrative, not measured research results.')
    f.panel(40, 48, 'a', 'Evidence-first workflow')
    nodes = [(65, 'Retrieve', C['blue']), (410, 'Evidence', C['purple']),
             (755, 'Review', C['orange']), (1100, 'Accept', C['teal'])]
    for x, label, color in nodes:
        f.rect(x, 133, 234, 117, 'white', color)
        f.text(x + 117, 204, label, 30, color, 600, 'middle')
        if x < 1100:
            f.arrow(x + 255, 192, x + 323)
    f.path('M872 267V321H527V268', C['purple'], 2.5)
    f.path('M521 278L527 268L533 278', C['purple'], 2.5)
    f.rect(618, 300, 160, 42, 'white', 'white', 0)
    f.text(698, 332, 'Recheck', 28, C['purple'], anchor='middle')
    f.path('M40 383H1360', C['light'], 1)

    f.panel(40, 443, 'b', 'Candidate retention')
    f.text(65, 504, 'Illustrative counts / 100', 27, C['muted'])
    for y, label, n, color in [(570, 'Method A', 82, C['blue']), (682, 'Method B', 74, C['gray'])]:
        f.text(65, y + 26, label, 28)
        f.rect(235, y - 4, n * 3.15, 40, color, color, 1)
        f.text(591, y + 27, n, 29, C['ink'], 600)
    f.path('M235 755H550', C['muted'], 1)
    for n in [0, 50, 100]:
        f.text(235 + n * 3.15, 797, n, 26, C['muted'], anchor='middle')
    f.path('M710 425V819', C['light'], 1)

    f.panel(770, 443, 'c', 'Review efficiency study')
    for y, label, color in [(533, 'Source browsing', C['muted']), (655, 'Evidence bundle', C['blue'])]:
        f.rect(795, y, 312, 68, 'white', color)
        f.text(951, y + 44, label, 28, color, anchor='middle')
    f.path('M1123 567H1151V689H1123', C['muted'], 2)
    f.arrow(1151, 628, 1203)
    f.text(1268, 607, 'Time', 28, anchor='middle')
    f.text(1268, 667, 'Errors', 28, anchor='middle')
    f.text(951, 795, 'Planned comparison', 26, C['muted'], anchor='middle')
    f.write(destination)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    build(args.out)
    print(args.out)
