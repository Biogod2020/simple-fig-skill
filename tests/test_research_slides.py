"""Companion slide-template browser checks; enable with RUN_RENDER_TESTS=1."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/simple-research-slides'
RENDER = SKILL / 'scripts/render_slides.cjs'
STARTER = SKILL / 'assets/starter.html'


@unittest.skipUnless(os.environ.get('RUN_RENDER_TESTS') == '1', 'Browser tests are opt-in')
class ResearchSlidesRenderTest(unittest.TestCase):
    def render(self, folder, source):
        file = Path(folder) / 'fixture.html'
        file.write_text(source)
        out = Path(folder) / 'output'
        run = subprocess.run(['node', str(RENDER), str(file), '--out-dir', str(out), '--strict'],
                             capture_output=True, text=True, timeout=30)
        report_file = out / 'render-check.json'
        report = json.loads(report_file.read_text()) if report_file.exists() else {}
        return run, report, out

    def test_starter_exports_all_pages_notes_and_synthetic_values(self):
        with tempfile.TemporaryDirectory() as folder:
            run, report, out = self.render(folder, STARTER.read_text())
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr + repr(report))
            self.assertEqual(report['slideCount'], 5)
            self.assertTrue(all(report['checks'].values()))
            self.assertEqual(report['timing']['seconds'], 420)
            self.assertEqual(len(list(out.glob('slide-*.png'))), 5)
            self.assertIn('数字和点都是人为构造', (out / 'speaker-notes.md').read_text())
            try:
                import fitz
            except ImportError:
                return
            with fitz.open(out / 'slides.pdf') as pdf:
                self.assertEqual(len(pdf), 5)
                self.assertAlmostEqual(pdf[0].rect.width / pdf[0].rect.height, 16 / 9, places=3)
                self.assertIn('构造', pdf[1].get_text())
                self.assertIn('比较 1', pdf[3].get_text())

    def test_bad_layout_and_external_asset_are_reported(self):
        faults = '<p data-qa style="position:absolute;left:1850px;top:200px;width:200px;height:35px;font-size:30px">' + ('Overflow ' * 35) + '</p>'
        faults += '<p data-qa style="position:absolute;left:104px;top:300px;width:900px;height:50px">Text over the title</p>'
        faults += '<img src="https://example.invalid/private.png" alt="blocked external image">'
        source = STARTER.read_text().replace('<aside class="notes">开场', faults + '<aside class="notes">开场', 1)
        with tempfile.TemporaryDirectory() as folder:
            run, report, _ = self.render(folder, source)
            self.assertEqual(run.returncode, 1)
            first = report['slides'][0]
            self.assertTrue(first['outside'])
            self.assertTrue(first['overflow'])
            self.assertTrue(first['overlaps'])
            self.assertTrue(first['unloadedImages'])
            self.assertEqual(report['blockedRequests'], ['https://example.invalid/private.png'])

    def test_print_only_overflow_is_not_hidden_by_screen_pass(self):
        source = STARTER.read_text().replace('</style>', '@media print{.source{height:8px!important}}\n</style>', 1)
        with tempfile.TemporaryDirectory() as folder:
            run, report, _ = self.render(folder, source)
            self.assertEqual(run.returncode, 1)
            self.assertFalse(any(s['overflow'] for s in report['slides']))
            self.assertTrue(any(s['overflow'] for s in report['printSlides']))

    def test_missing_interface_produces_a_failure_receipt(self):
        source = STARTER.read_text().replace('window.simpleSlides={show,', 'window.otherInterface={show,')
        with tempfile.TemporaryDirectory() as folder:
            run, report, _ = self.render(folder, source)
            self.assertEqual(run.returncode, 1)
            self.assertIn('window.simpleSlides', report['error'])


if __name__ == '__main__':
    unittest.main()
