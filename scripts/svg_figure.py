"""Small native-SVG primitives for concise scientific figures (stdlib only)."""

import base64
import math
from html import escape
from pathlib import Path

COLORS = {
    'ink': '#202937', 'muted': '#697586', 'blue': '#3164AD',
    'purple': '#7962AB', 'teal': '#21877B', 'orange': '#BF642F',
    'gray': '#98A3B1', 'light': '#DCE2E9', 'white': '#FFFFFF',
}


def finite(*values: float) -> None:
    """Reject invalid geometry rather than producing an unreadable SVG."""
    if not all(math.isfinite(v) for v in values):
        raise ValueError('SVG geometry must be finite')


class SvgFigure:
    """Build one editable figure; units scale with its viewBox."""

    def __init__(self, width: float = 1400, height: float = 850,
                 description: str = '') -> None:
        finite(width, height)
        if width <= 0 or height <= 0:
            raise ValueError('Canvas dimensions must be positive')
        self.width = width
        self.height = height
        self.parts: list[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">',
            f'<desc>{escape(description)}</desc>',
            f'<rect width="{width}" height="{height}" fill="white"/>',
        ]
        self.letters: set[str] = set()

    def text(self, x: float, y: float, value: object, size: float = 28,
             color: str = COLORS['ink'], weight: int = 400,
             anchor: str = 'start', css_class: str = '') -> None:
        finite(x, y, size)
        if size <= 0 or anchor not in {'start', 'middle', 'end'}:
            raise ValueError('Invalid text size or anchor')
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" '
            f'font-size="{size}" fill="{escape(color, quote=True)}" font-weight="{weight}" '
            f'text-anchor="{anchor}" class="{escape(css_class, quote=True)}">'
            f'{escape(str(value))}</text>')

    def panel(self, x: float, y: float, letter: str, title: str) -> None:
        if not letter or letter in self.letters or not title.strip():
            raise ValueError('Each panel needs a unique nonempty letter and one title')
        self.letters.add(letter)
        self.text(x, y, letter, 33, weight=700, css_class='panel-letter')
        self.text(x + 37, y, title, 31, weight=600, css_class='panel-title')

    def rect(self, x: float, y: float, width: float, height: float,
             fill: str = 'white', stroke: str = COLORS['light'],
             radius: float = 6, stroke_width: float = 2) -> None:
        finite(x, y, width, height, radius, stroke_width)
        if min(width, height, radius, stroke_width) < 0:
            raise ValueError('Rectangle sizes must not be negative')
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" '
            f'fill="{escape(fill, quote=True)}" stroke="{escape(stroke, quote=True)}" '
            f'stroke-width="{stroke_width}"/>')

    def path(self, d: str, color: str = COLORS['muted'], width: float = 2,
             fill: str = 'none', dash: str = '') -> None:
        finite(width)
        if width < 0:
            raise ValueError('Stroke width must not be negative')
        self.parts.append(
            f'<path d="{escape(d, quote=True)}" fill="{escape(fill, quote=True)}" '
            f'stroke="{escape(color, quote=True)}" stroke-width="{width}" '
            f'stroke-dasharray="{escape(dash, quote=True)}"/>')

    def arrow(self, x1: float, y: float, x2: float,
              color: str = COLORS['muted']) -> None:
        finite(x1, y, x2)
        direction = 1 if x2 >= x1 else -1
        self.path(f'M{x1} {y}H{x2}', color, 2.5)
        self.path(f'M{x2-10*direction} {y-6}L{x2} {y}L{x2-10*direction} {y+6}', color, 2.5)

    def circle(self, x: float, y: float, radius: float,
               fill: str = COLORS['blue']) -> None:
        finite(x, y, radius)
        if radius < 0:
            raise ValueError('Radius must not be negative')
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{escape(fill, quote=True)}"/>')

    def image(self, source: Path, x: float, y: float, width: float, height: float) -> None:
        """Embed the original raster bytes with aspect ratio preserved, without cropping."""
        finite(x, y, width, height)
        if width <= 0 or height <= 0:
            raise ValueError('Image viewport must be positive')
        mime = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                '.webp': 'image/webp', '.gif': 'image/gif'}.get(source.suffix.lower())
        if mime is None:
            raise ValueError('Embed a PNG, JPEG, WebP or GIF; compose SVG assets as vectors')
        encoded = base64.b64encode(source.read_bytes()).decode('ascii')
        self.parts.append(f'<image x="{x}" y="{y}" width="{width}" height="{height}" '
                          f'preserveAspectRatio="xMidYMid meet" href="data:{mime};base64,{encoded}"/>')

    def write(self, destination: Path) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text('\n'.join(self.parts + ['</svg>']), encoding='utf-8')
