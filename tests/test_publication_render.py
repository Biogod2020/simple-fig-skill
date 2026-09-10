"""Publication-mode regressions; browser tests require RUN_RENDER_TESTS=1."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RENDER = ROOT / 'scripts' / 'render_svg.cjs'
sys.path.insert(0, str(ROOT / 'scripts'))
from make_evidence_example import COHORTS, PER_COHORT, build


class ExampleTest(unittest.TestCase):
    def test_demo_is_reproducible_and_disclosed(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / 'demo.svg'
            build(file)
            first = file.read_bytes()
            build(file)
            self.assertEqual(first, file.read_bytes())
            root = ET.parse(file).getroot()
            ns = '{http://www.w3.org/2000/svg}'
            self.assertIn('not experimental data', root.find(ns + 'desc').text)
            titles = [n for n in root.iter(ns + 'text') if n.get('class') == 'panel-title']
            self.assertEqual(len(titles), 3)
            self.assertEqual(sum(row[1] for row in COHORTS), 171)
            self.assertEqual(sum(row[2] for row in COHORTS), 190)
            self.assertTrue(any(b < a for _, a, b in COHORTS))
            self.assertTrue(all(0 <= a <= PER_COHORT and 0 <= b <= PER_COHORT for _, a, b in COHORTS))


@unittest.skipUnless(os.environ.get('RUN_RENDER_TESTS') == '1', 'Browser tests are opt-in')
class PublicationRenderTest(unittest.TestCase):
    def run_fixture(self, folder, body, *args):
        file = Path(folder) / 'fixture.svg'
        file.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180">' + body + '</svg>')
        run = subprocess.run(['node', str(RENDER), str(file), *args], capture_output=True, text=True, timeout=30)
        report_file = file.with_suffix('.render-check.json')
        report = json.loads(report_file.read_text()) if report_file.exists() else {}
        return run, report, file

    def test_final_size_and_large_text_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            run, report, file = self.run_fixture(directory, '<text x="20" y="70" font-size="20">Readable</text>', '--width-mm', '89', '--strict')
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr + repr(report))
            self.assertEqual(report['font_check']['status'], 'PASS')
            self.assertAlmostEqual(report['font_check']['minimum_pt'], 20 * 89 * 72 / 25.4 / 320, places=2)
            # PyMuPDF is optional: the browser itself has no new dependency.
            try:
                import fitz
            except ImportError:
                return
            with fitz.open(file.with_suffix('.pdf')) as pdf:
                self.assertEqual(len(pdf), 1)
                self.assertAlmostEqual(pdf[0].rect.width * 25.4 / 72, 89, delta=0.4)
                self.assertIn('Readable', pdf[0].get_text())

    def test_transformed_tspan_small_text_is_detected(self):
        body = '<g transform="translate(30 80) scale(0.5)"><text font-size="20">R<tspan font-size="10">2</tspan></text></g>'
        with tempfile.TemporaryDirectory() as directory:
            run, report, _ = self.run_fixture(directory, body, '--width-mm', '89', '--strict')
            self.assertEqual(run.returncode, 1)
            self.assertEqual(report['font_check']['status'], 'REVIEW REQUIRED')
            self.assertTrue(any(row['text'] == '2' for row in report['font_check']['small_text']))

    def test_collisions_warn_or_fail_without_changing_artwork(self):
        body = '<text x="20" y="60" font-size="20">First</text><text x="24" y="60" font-size="20">Second</text>'
        with tempfile.TemporaryDirectory() as directory:
            run, report, _ = self.run_fixture(directory, body)
            self.assertEqual(run.returncode, 0)
            self.assertEqual(len(report['text_collisions']), 1)
            run, report, _ = self.run_fixture(directory, body, '--strict')
            self.assertEqual(run.returncode, 1)

    def test_raster_only_is_not_a_font_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            run, report, _ = self.run_fixture(directory, '<rect width="100" height="50"/>', '--width-mm', '89', '--strict')
            self.assertEqual(run.returncode, 1)
            self.assertEqual(report['font_check']['status'], 'NOT AUDITABLE')

    def test_print_only_tiny_text_is_checked(self):
        body = '<style>@media print{text{font-size:2px}}</style><text x="20" y="60" font-size="20">Print</text>'
        with tempfile.TemporaryDirectory() as directory:
            run, report, _ = self.run_fixture(directory, body, '--width-mm', '89', '--strict')
            self.assertEqual(run.returncode, 1)
            self.assertTrue(report['font_check']['small_text'])

    def test_bad_width_is_rejected_before_browser_launch(self):
        for value in ['0', '-1', 'NaN', 'Infinity', 'missing']:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                run, _, _ = self.run_fixture(directory, '', '--width-mm', value)
                self.assertEqual(run.returncode, 1)
                self.assertIn('positive finite number', run.stderr)

    def test_complete_demo_passes_at_double_column_size(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / 'demo.svg'
            build(file)
            run = subprocess.run(['node', str(RENDER), str(file), '--width-mm', '180', '--strict'], capture_output=True, text=True, timeout=30)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            report = json.loads(file.with_suffix('.render-check.json').read_text())
            self.assertEqual(report['canvas_overflow'], [])
            self.assertEqual(report['text_collisions'], [])


if __name__ == '__main__':
    unittest.main()
