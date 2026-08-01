import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from repository_ai_ready_issue_triage_board_20260801.cli import build_rows, main, recommendation, score_issue


class ScoreTests(unittest.TestCase):
    def test_scores_specific_issue_higher_than_sensitive_vague_issue(self):
        good = {'title': 'Crash on save', 'body': 'Steps to repro with traceback in app.py line 4', 'labels': ['agent-ready']}
        bad = {'title': 'Rewrite auth', 'body': 'Sometimes broken. token and password involved', 'labels': []}
        self.assertGreater(score_issue(good)[0], score_issue(bad)[0])

    def test_recommendation_marks_clear_high_score_as_agent_ready(self):
        score, reasons = score_issue({'title': 'Crash on save', 'body': 'Steps to repro with traceback in app.py line 4', 'labels': ['agent-ready']})
        self.assertEqual(recommendation(score, reasons), 'delegate_to_agent')

    def test_build_rows_includes_recommendation_and_sorting(self):
        rows = build_rows([
            {'number': 2, 'title': 'Rewrite auth', 'body': 'Sometimes broken. token involved', 'labels': []},
            {'number': 1, 'title': 'Crash on save', 'body': 'Steps to repro with traceback in app.py line 4', 'labels': ['agent-ready']},
        ])
        self.assertEqual(rows[0]['number'], 1)
        self.assertEqual(rows[0]['recommendation'], 'delegate_to_agent')
        self.assertIn('recommendation', rows[1])

    def test_main_json_format(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'issues.json'
            path.write_text(json.dumps([{'number': 1, 'title': 'Crash', 'body': 'Steps to repro with traceback', 'labels': ['agent-ready']}]), encoding='utf-8')
            with patch('builtins.print') as mocked_print:
                main([str(path), '--format', 'json'])
        payload = json.loads(mocked_print.call_args.args[0])
        self.assertEqual(payload['issues'][0]['recommendation'], 'delegate_to_agent')


if __name__ == '__main__':
    unittest.main()
