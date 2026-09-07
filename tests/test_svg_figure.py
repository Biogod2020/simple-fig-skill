"""Behavior checks for XML text, finite geometry and image preservation."""

import base64
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from svg_figure import SvgFigure

NS = '{http://www.w3.org/2000/svg}'


class SvgFigureTest(unittest.TestCase):
    def test_text_is_preserved_without_xml_injection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'figure.svg'
            figure = SvgFigure(description='A & B')
            value = 'H&E <source> "配对"'
            figure.text(30, 60, value)
            figure.write(target)
            root = ET.parse(target).getroot()
            self.assertEqual(root.find(NS + 'text').text, value)
            self.assertIsNone(root.find(NS + 'source'))

    def test_invalid_geometry_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            SvgFigure(float('nan'), 100)
        with self.assertRaises(ValueError):
            SvgFigure().rect(0, 0, -1, 20)
        with self.assertRaises(ValueError):
            SvgFigure().text(0, 0, 'label', float('inf'))

    def test_raster_bytes_are_embedded_without_changes(self) -> None:
        raw = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aL1kAAAAASUVORK5CYII=')
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'pixel.png'
            target = Path(directory) / 'figure.svg'
            source.write_bytes(raw)
            figure = SvgFigure()
            figure.image(source, 10, 20, 200, 100)
            figure.write(target)
            image = ET.parse(target).getroot().find(NS + 'image')
            self.assertEqual(base64.b64decode(image.get('href').split(',', 1)[1]), raw)
            self.assertEqual(image.get('preserveAspectRatio'), 'xMidYMid meet')


if __name__ == '__main__':
    unittest.main()
