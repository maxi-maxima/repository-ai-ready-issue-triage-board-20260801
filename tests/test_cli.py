import unittest

from repository_ai_ready_issue_triage_board_20260801.cli import score_issue


class ScoreTests(unittest.TestCase):
    def test_scores_specific_issue_higher_than_sensitive_vague_issue(self):
        good = {'title': 'Crash on save', 'body': 'Steps to repro with traceback in app.py line 4', 'labels': ['agent-ready']}
        bad = {'title': 'Rewrite auth', 'body': 'Sometimes broken. token and password involved', 'labels': []}
        self.assertGreater(score_issue(good)[0], score_issue(bad)[0])


if __name__ == '__main__':
    unittest.main()
