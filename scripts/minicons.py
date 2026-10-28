"""Small flat vector icons for scientific figures, so files, tools and objects read at a glance.
Drawn as SVG paths, not emoji glyphs, so they print identically in every PDF viewer and pass text audits.
Each function takes the top-left corner (x, y) and the box size s in figure units (0.1 mm) and returns an SVG string.
"""
from __future__ import annotations

import math

BLUE, NAVY, TEAL, PINK, GREY, INK = "#3164ad", "#1f4e79", "#2a9d8f", "#c96f8e", "#8a8f98", "#3a4250"


def _doc(x: float, y: float, s: float, col: str) -> str:
    """A document with a folded corner, outlined in col."""
    w, h, c = s * 0.78, s, s * 0.24
    x0 = x + (s - w) / 2
    return (f'<path d="M{x0:.1f},{y:.1f} L{x0 + w - c:.1f},{y:.1f} L{x0 + w:.1f},{y + c:.1f} L{x0 + w:.1f},{y + h:.1f} '
            f'L{x0:.1f},{y + h:.1f} Z" fill="#ffffff" stroke="{col}" stroke-width="{max(s * 0.06, 1.2):.1f}" '
            f'stroke-linejoin="round"/>'
            f'<path d="M{x0 + w - c:.1f},{y:.1f} L{x0 + w - c:.1f},{y + c:.1f} L{x0 + w:.1f},{y + c:.1f}" fill="none" '
            f'stroke="{col}" stroke-width="{max(s * 0.05, 1.0):.1f}"/>')


def h5ad(x: float, y: float, s: float = 28) -> str:
    """spatial.h5ad: a document holding a hexagonal spot array coloured by expression."""
    out = [_doc(x, y, s, BLUE)]
    r = s * 0.065
    cols = ["#c5d5ee", "#5b86c4", "#1f4e79", "#86a7d6"]
    k = 0
    for j in range(3):
        for i in range(3):
            cx = x + s * 0.30 + i * s * 0.2 + (s * 0.1 if j % 2 else 0)
            cy = y + s * 0.38 + j * s * 0.19
            out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{cols[k % 4]}"/>')
            k += 1
    return "".join(out)


def tif(x: float, y: float, s: float = 28) -> str:
    """image.tif: a framed picture with a pink tissue section."""
    w, h = s, s * 0.82
    y0 = y + (s - h) / 2
    blob = (f'M{x + s * .22:.1f},{y0 + h * .62:.1f} C{x + s * .18:.1f},{y0 + h * .30:.1f} {x + s * .48:.1f},'
            f'{y0 + h * .18:.1f} {x + s * .66:.1f},{y0 + h * .30:.1f} C{x + s * .86:.1f},{y0 + h * .42:.1f} '
            f'{x + s * .80:.1f},{y0 + h * .78:.1f} {x + s * .56:.1f},{y0 + h * .78:.1f} C{x + s * .40:.1f},'
            f'{y0 + h * .80:.1f} {x + s * .26:.1f},{y0 + h * .82:.1f} {x + s * .22:.1f},{y0 + h * .62:.1f} Z')
    return (f'<rect x="{x:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{s * .08:.1f}" fill="#fbf3f6" '
            f'stroke="{PINK}" stroke-width="{max(s * 0.06, 1.2):.1f}"/>'
            f'<path d="{blob}" fill="#d98aa6"/>'
            f'<circle cx="{x + s * .46:.1f}" cy="{y0 + h * .50:.1f}" r="{s * .07:.1f}" fill="#9c3f63"/>')


def json_(x: float, y: float, s: float = 28) -> str:
    """sample.json: a document with curly braces and a key line."""
    out = [_doc(x, y, s, GREY)]
    sw = max(s * 0.06, 1.2)
    cx0, cx1, cy = x + s * 0.33, x + s * 0.67, y + s * 0.6
    hh = s * 0.2
    for cx_, d in ((cx0, 1), (cx1, -1)):
        out.append(f'<path d="M{cx_ + d * s * .06:.1f},{cy - hh:.1f} Q{cx_:.1f},{cy - hh:.1f} {cx_:.1f},{cy - hh * .4:.1f} '
                   f'Q{cx_:.1f},{cy:.1f} {cx_ - d * s * .06:.1f},{cy:.1f} Q{cx_:.1f},{cy:.1f} {cx_:.1f},{cy + hh * .4:.1f} '
                   f'Q{cx_:.1f},{cy + hh:.1f} {cx_ + d * s * .06:.1f},{cy + hh:.1f}" fill="none" stroke="{INK}" '
                   f'stroke-width="{sw:.1f}" stroke-linecap="round"/>')
    out.append(f'<circle cx="{x + s * .5:.1f}" cy="{cy:.1f}" r="{s * .045:.1f}" fill="{INK}"/>')
    return "".join(out)


def magnifier(x: float, y: float, s: float = 24, col: str = BLUE) -> str:
    r = s * 0.3
    cx, cy = x + s * 0.42, y + s * 0.42
    sw = max(s * 0.09, 1.4)
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="#eef3fb" stroke="{col}" stroke-width="{sw:.1f}"/>'
            f'<path d="M{cx + r * .72:.1f},{cy + r * .72:.1f} L{x + s * .92:.1f},{y + s * .92:.1f}" stroke="{col}" '
            f'stroke-width="{sw * 1.3:.1f}" stroke-linecap="round"/>')


def eye(x: float, y: float, s: float = 24, col: str = PINK) -> str:
    cy = y + s / 2
    sw = max(s * 0.08, 1.3)
    return (f'<path d="M{x + s * .04:.1f},{cy:.1f} Q{x + s / 2:.1f},{cy - s * .5:.1f} {x + s * .96:.1f},{cy:.1f} '
            f'Q{x + s / 2:.1f},{cy + s * .5:.1f} {x + s * .04:.1f},{cy:.1f} Z" fill="#ffffff" stroke="{col}" '
            f'stroke-width="{sw:.1f}" stroke-linejoin="round"/>'
            f'<circle cx="{x + s / 2:.1f}" cy="{cy:.1f}" r="{s * .16:.1f}" fill="{col}"/>')


def code(x: float, y: float, s: float = 24, col: str = INK) -> str:
    """</> brackets."""
    sw = max(s * 0.09, 1.4)
    cy = y + s / 2
    return (f'<path d="M{x + s * .30:.1f},{cy - s * .26:.1f} L{x + s * .06:.1f},{cy:.1f} L{x + s * .30:.1f},{cy + s * .26:.1f} '
            f'M{x + s * .70:.1f},{cy - s * .26:.1f} L{x + s * .94:.1f},{cy:.1f} L{x + s * .70:.1f},{cy + s * .26:.1f} '
            f'M{x + s * .58:.1f},{cy - s * .34:.1f} L{x + s * .42:.1f},{cy + s * .34:.1f}" fill="none" stroke="{col}" '
            f'stroke-width="{sw:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')


def terminal(x: float, y: float, s: float = 24, col: str = INK) -> str:
    sw = max(s * 0.08, 1.3)
    h = s * 0.8
    y0 = y + (s - h) / 2
    return (f'<rect x="{x:.1f}" y="{y0:.1f}" width="{s:.1f}" height="{h:.1f}" rx="{s * .1:.1f}" fill="{col}"/>'
            f'<path d="M{x + s * .2:.1f},{y0 + h * .32:.1f} L{x + s * .38:.1f},{y0 + h * .5:.1f} L{x + s * .2:.1f},'
            f'{y0 + h * .68:.1f} M{x + s * .48:.1f},{y0 + h * .7:.1f} L{x + s * .78:.1f},{y0 + h * .7:.1f}" fill="none" '
            f'stroke="#ffffff" stroke-width="{sw:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')


def check(x: float, y: float, s: float = 24, col: str = NAVY) -> str:
    """A passed check: filled circle with a white tick."""
    r = s / 2
    cx, cy = x + r, y + r
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{col}"/>'
            f'<path d="M{cx - r * .45:.1f},{cy + r * .02:.1f} L{cx - r * .1:.1f},{cy + r * .38:.1f} L{cx + r * .5:.1f},'
            f'{cy - r * .36:.1f}" fill="none" stroke="#ffffff" stroke-width="{r * .3:.1f}" stroke-linecap="round" '
            f'stroke-linejoin="round"/>')


def clock(x: float, y: float, s: float = 24, col: str = GREY) -> str:
    r = s * 0.44
    cx, cy = x + s / 2, y + s / 2
    sw = max(s * 0.08, 1.3)
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="#ffffff" stroke="{col}" stroke-width="{sw:.1f}"/>'
            f'<path d="M{cx:.1f},{cy - r * .6:.1f} L{cx:.1f},{cy:.1f} L{cx + r * .45:.1f},{cy + r * .3:.1f}" fill="none" '
            f'stroke="{INK}" stroke-width="{sw:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')


def idcard(x: float, y: float, s: float = 28, col: str = GREY) -> str:
    """Sample identity: a card with a portrait disc and two lines."""
    h = s * 0.7
    y0 = y + (s - h) / 2
    sw = max(s * 0.06, 1.2)
    return (f'<rect x="{x:.1f}" y="{y0:.1f}" width="{s:.1f}" height="{h:.1f}" rx="{s * .08:.1f}" fill="#ffffff" '
            f'stroke="{col}" stroke-width="{sw:.1f}"/>'
            f'<circle cx="{x + s * .27:.1f}" cy="{y0 + h * .45:.1f}" r="{s * .12:.1f}" fill="#c5d5ee"/>'
            f'<path d="M{x + s * .48:.1f},{y0 + h * .36:.1f} L{x + s * .84:.1f},{y0 + h * .36:.1f} M{x + s * .48:.1f},'
            f'{y0 + h * .6:.1f} L{x + s * .74:.1f},{y0 + h * .6:.1f}" stroke="{INK}" stroke-width="{sw:.1f}" '
            f'stroke-linecap="round"/>')


def archive(x: float, y: float, s: float = 28, col: str = "#b08a4a") -> str:
    """An archive (.tar, .zip): a box with a zipper strip."""
    sw = max(s * 0.06, 1.2)
    return (f'<rect x="{x:.1f}" y="{y + s * .28:.1f}" width="{s:.1f}" height="{s * .66:.1f}" rx="{s * .06:.1f}" '
            f'fill="#f3e6cc" stroke="{col}" stroke-width="{sw:.1f}"/>'
            f'<rect x="{x - s * .04:.1f}" y="{y + s * .12:.1f}" width="{s * 1.08:.1f}" height="{s * .2:.1f}" '
            f'rx="{s * .05:.1f}" fill="#e4cd9c" stroke="{col}" stroke-width="{sw:.1f}"/>'
            + "".join(f'<rect x="{x + s * .44:.1f}" y="{y + s * (.34 + k * .12):.1f}" width="{s * .12:.1f}" '
                      f'height="{s * .07:.1f}" fill="{col}"/>' for k in range(4)))


def flask(x: float, y: float, s: float = 24, col: str = TEAL) -> str:
    """Scoring / tests."""
    sw = max(s * 0.08, 1.3)
    return (f'<path d="M{x + s * .36:.1f},{y + s * .08:.1f} L{x + s * .36:.1f},{y + s * .40:.1f} L{x + s * .1:.1f},'
            f'{y + s * .9:.1f} L{x + s * .9:.1f},{y + s * .9:.1f} L{x + s * .64:.1f},{y + s * .40:.1f} L{x + s * .64:.1f},'
            f'{y + s * .08:.1f}" fill="#e3f2ef" stroke="{col}" stroke-width="{sw:.1f}" stroke-linejoin="round"/>'
            f'<path d="M{x + s * .22:.1f},{y + s * .68:.1f} L{x + s * .78:.1f},{y + s * .68:.1f} L{x + s * .9:.1f},'
            f'{y + s * .9:.1f} L{x + s * .1:.1f},{y + s * .9:.1f} Z" fill="{col}"/>')


def ruler(x: float, y: float, s: float = 24, col: str = "#b08a4a") -> str:
    """Units / scale (µm)."""
    sw = max(s * 0.07, 1.2)
    out = [f'<rect x="{x:.1f}" y="{y + s * .3:.1f}" width="{s:.1f}" height="{s * .4:.1f}" rx="{s * .05:.1f}" '
           f'fill="#f3e6cc" stroke="{col}" stroke-width="{sw:.1f}"/>']
    for k in range(1, 6):
        xx = x + k * s / 6
        out.append(f'<path d="M{xx:.1f},{y + s * .3:.1f} L{xx:.1f},{y + s * (.46 if k % 2 else .54):.1f}" '
                   f'stroke="{col}" stroke-width="{sw:.1f}"/>')
    return "".join(out)


def quote(x: float, y: float, s: float = 24, col: str = GREY) -> str:
    """A cited GEO quote: speech-mark glyph drawn as two filled commas."""
    out = []
    for dx in (0.18, 0.56):
        cx, cy = x + s * (dx + .12), y + s * .38
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{s * .13:.1f}" fill="{col}"/>'
                   f'<path d="M{cx + s * .1:.1f},{cy:.1f} Q{cx + s * .1:.1f},{cy + s * .3:.1f} {cx - s * .12:.1f},'
                   f'{cy + s * .36:.1f}" fill="none" stroke="{col}" stroke-width="{s * .09:.1f}" stroke-linecap="round"/>')
    return "".join(out)


FILE_ICON = {"spatial.h5ad": h5ad, "image.tif": tif, "sample.json": json_}
TOOL_ICON = {"file inspection": magnifier, "image viewing": eye, "code revision": code, "execution": terminal,
             "scoring": flask, "run records": clock}
