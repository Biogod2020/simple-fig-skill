"""Optional browser integration tests: RUN_RENDER_TESTS=1 enables them."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

RENDER = Path(__file__).resolve().parents[1] / 'scripts' / 'render_svg.cjs'


@unittest.skipUnless(os.environ.get('RUN_RENDER_TESTS') == '1', 'Browser tests are opt-in')
class RenderSvgTest(unittest.TestCase):
    def render(self, folder: Path, body: str) -> tuple[subprocess.CompletedProcess, dict]:
        source = folder / 'fixture.svg'
        source.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180">' + body + '</svg>')
        result = subprocess.run(['node', str(RENDER), str(source)], capture_output=True, text=True, timeout=60)
        report = json.loads(source.with_suffix('.render-check.json').read_text())
        return result, report

    def test_rotated_label_inside_canvas_is_not_a_false_positive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            result, report = self.render(folder, '<g transform="translate(80 120) rotate(-90)"><text font-size="28">Axis</text></g>')
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(report['canvas_overflow'], [])
            self.assertTrue((folder / 'fixture.pdf').read_bytes().startswith(b'%PDF'))

    def test_translated_label_outside_canvas_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result, report = self.render(Path(directory), '<g transform="translate(290 100)"><text font-size="28">Outside</text></g>')
            self.assertEqual(result.returncode, 1)
            self.assertEqual(len(report['canvas_overflow']), 1)

    def test_unembedded_image_is_an_explicit_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result, report = self.render(Path(directory), '<image href="missing.png" width="100" height="100"/>')
            self.assertEqual(result.returncode, 1)
            self.assertIn('external references', report['error'])


if __name__ == '__main__':
    unittest.main()
