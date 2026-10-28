"""Every icon renders as well-formed SVG with finite coordinates."""

from pathlib import Path
import math
import re
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import minicons as mi

ICONS = [mi.h5ad, mi.tif, mi.json_, mi.magnifier, mi.eye, mi.code, mi.terminal, mi.check, mi.clock,
         mi.idcard, mi.archive, mi.flask, mi.ruler, mi.quote]


class MiniconsTest(unittest.TestCase):
    def test_icons_are_wellformed_and_finite(self) -> None:
        for fn in ICONS:
            svg = fn(10, 20, 24)
            ET.fromstring(f'<svg xmlns="http://www.w3.org/2000/svg">{svg}</svg>')
            for num in re.findall(r'-?\d+(?:\.\d+)?', svg):
                self.assertTrue(math.isfinite(float(num)), fn.__name__)

    def test_lookup_tables_cover_named_files_and_tools(self) -> None:
        self.assertEqual(set(mi.FILE_ICON), {'spatial.h5ad', 'image.tif', 'sample.json'})
        self.assertIn('scoring', mi.TOOL_ICON)


if __name__ == '__main__':
    unittest.main()
