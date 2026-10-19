from datetime import datetime, timedelta, timezone
from decimal import localcontext
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from wealth_platform.core import Registry, Snapshot, ValidationError, calculate, digest
from wealth_platform.workflow import Workflow

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 10, 19, 12, tzinfo=timezone.utc)

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'examples/matched.json').read_text())
        self.metric = Registry().get('synthetic_nav', '1.0.0')

    def calc(self, data=None):
        return calculate(Snapshot.parse(self.data if data is None else data, self.metric, NOW), self.metric)

    def test_reference_and_hash(self):
        self.assertEqual(self.calc()['actual'], '1000000.00')
        self.assertEqual(digest(self.data), digest(dict(reversed(list(self.data.items())))))

    def test_rounding_and_negative_nav(self):
        for assets, liabilities, expected in [('1.005', '0', '1.00'), ('1.015', '0', '1.02'), ('1', '2', '-1.00')]:
            self.data.update(assets=assets, liabilities=liabilities, expected=expected)
            self.assertEqual(self.calc()['actual'], expected)

    def test_tolerance_boundary(self):
        for expected, status in [('999999.99', 'matched'), ('999999.98', 'exception')]:
            self.data['expected'] = expected
            self.assertEqual(self.calc()['reconciliation'], status)

    def test_reject_ambiguous_amounts(self):
        for value in [1.1, True, 'NaN', 'Infinity', '1e9', '1.1234567', '9'*19, '-1', ' 1']:
            with self.subTest(value=value), self.assertRaises(ValidationError):
                self.calc({**self.data, 'assets': value})

    def test_contract_failures(self):
        for field, value in [('synthetic', False), ('synthetic', 1), ('currency', 'EUR'), ('schema_version', '2'), ('period', '2025-01-01'), ('period', '2026-10-20'), ('period', '20261018'), ('extracted_at', '2026-10-19T10:00:00'), ('snapshot_id', ''), ('entity_id', [])]:
            with self.subTest(field=field, value=value), self.assertRaises(ValidationError):
                self.calc({**self.data, field: value})

    def test_missing_extra_fields(self):
        missing = dict(self.data)
        del missing['assets']
        for data in [missing, {**self.data, 'extra': 1}, []]:
            with self.assertRaises(ValidationError):
                self.calc(data)

    def test_freshness(self):
        for hours in [-1, 24.001]:
            with self.assertRaises(ValidationError):
                self.calc({**self.data, 'extracted_at': (NOW-timedelta(hours=hours)).isoformat(), 'period': '2026-10-17'})
        self.calc({**self.data, 'extracted_at': (NOW-timedelta(hours=24)).isoformat()})

    def test_timezone(self):
        self.assertEqual(self.calc({**self.data, 'extracted_at': '2026-10-19T06:00:00-04:00'}), self.calc())

    def test_reference_precision(self):
        with self.assertRaises(ValidationError):
            self.calc({**self.data, 'expected': '1000000.001'})

    def test_unknown_metric(self):
        with self.assertRaises(ValidationError):
            Registry().get('synthetic_nav', '2.0.0')

    def test_decimal_context(self):
        with localcontext() as context:
            context.prec = 3
            self.assertEqual(self.calc()['actual'], '1000000.00')

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = str(Path(self.tmp.name)/'test.sqlite3')
        self.workflow = Workflow(self.path)
        self.addCleanup(self.workflow.close)
        self.data = json.loads((ROOT/'examples/matched.json').read_text())

    def submit(self):
        return self.workflow.submit(self.data, run_id='run-001', actor='analyst', now=NOW)

    def review(self, **kwargs):
        args = dict(reviewer='reviewer', decision='approved', evidence='Synthetic reference confirmed.')
        args.update(kwargs)
        return self.workflow.review('run-001', **args)

    def test_full_run_review_persistence(self):
        run = self.submit()
        self.assertEqual(run['state'], 'pending_review')
        self.assertEqual(run['lineage']['source_sha256'], digest(self.data))
        reviewed = self.review()
        self.assertEqual(reviewed['state'], 'approved')
        with Workflow(self.path) as reopened:
            self.assertEqual(reopened.get('run-001'), reviewed)

    def test_exception_preserved(self):
        self.data['expected'] = '999900.00'
        self.assertEqual(self.submit()['result']['delta'], '100.00')
        run = self.review(decision='rejected')
        self.assertEqual(run['result']['reconciliation'], 'exception')
        self.assertEqual(run['state'], 'rejected')

    def test_replay(self):
        first = self.submit()
        replay = self.workflow.submit(self.data, run_id='run-001', actor='analyst', now=NOW+timedelta(days=30))
        self.assertEqual(first, replay)
        self.assertEqual(len(self.workflow.list()), 1)

    def test_conflict(self):
        self.submit()
        self.data['expected'] = '1.00'
        with self.assertRaises(ValidationError):
            self.submit()
        self.assertEqual(len(self.workflow.list()), 1)

    def test_invalid_not_persisted(self):
        self.data['assets'] = 'NaN'
        with self.assertRaises(ValidationError):
            self.submit()
        self.assertEqual(self.workflow.list(), [])

    def test_self_review(self):
        self.submit()
        with self.assertRaises(ValidationError):
            self.review(reviewer='analyst')
        self.assertEqual(self.workflow.get('run-001')['state'], 'pending_review')

    def test_review_validation(self):
        self.submit()
        for kwargs in [dict(evidence=''), dict(decision='approve')]:
            with self.assertRaises(ValidationError):
                self.review(**kwargs)

    def test_review_final(self):
        self.submit()
        self.review()
        with self.assertRaises(ValidationError):
            self.review(decision='rejected')

    def test_unknown_run(self):
        with self.assertRaises(ValidationError):
            self.workflow.get('missing')

    def cli(self, *args):
        return subprocess.run([sys.executable, '-m', 'wealth_platform', '--db', self.path, *args], capture_output=True, text=True)

    def test_cli_flow(self):
        run = self.cli('run', str(ROOT/'examples/exception.json'), '--run-id', 'cli-001', '--actor', 'analyst', '--as-of', NOW.isoformat())
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['result']['reconciliation'], 'exception')
        review = self.cli('review', 'cli-001', '--reviewer', 'reviewer', '--decision', 'rejected', '--evidence', 'Synthetic discrepancy requires correction.')
        self.assertEqual(review.returncode, 0, review.stderr)
        self.assertEqual(json.loads(self.cli('show', 'cli-001').stdout)['state'], 'rejected')

    def test_cli_duplicate_json(self):
        path = Path(self.tmp.name)/'duplicate.json'
        path.write_text('{"assets":"1", "assets":"2"}')
        result = self.cli('run', str(path), '--run-id', 'bad', '--actor', 'analyst')
        self.assertEqual(result.returncode, 2)
        self.assertIn('duplicate JSON field', result.stderr)

if __name__ == '__main__':
    unittest.main()
