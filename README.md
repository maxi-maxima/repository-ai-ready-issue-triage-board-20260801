# Repository AI-Ready Issue Triage Board

Maintainers want AI agents to help, but not every issue is safe or specific enough to delegate. This CLI ranks issues by agent readiness and flags privacy or scope risks.

## Why now

GitHub and developer communities are pushing issue-to-PR agents, automated triage, and multi-agent coding teams. The bottleneck is choosing the right work, not merely starting more agents.

## Install and run

```bash
python -m repository_ai_ready_issue_triage_board_20260801.cli examples/issues.json
python -m repository_ai_ready_issue_triage_board_20260801.cli examples/issues.json --format json
python -m repository_ai_ready_issue_triage_board_20260801.cli examples/issues.json --format markdown
python -m repository_ai_ready_issue_triage_board_20260801.cli examples/issues.json --forbid-label security --forbid-label legal
python -m unittest discover -s tests
```

Repeat `--forbid-label` to keep matching issues human-owned regardless of their
readiness score. Label matching is case-insensitive and exact. Inputs may use
plain label names or GitHub REST API label objects.

## Example

```csv
number,score,recommendation,title,reasons
12,95,delegate_to_agent,Crash on save,has reproduction clues; has concrete evidence; label suggests delegation
```

Markdown output is available for project boards and issue comments:

```markdown
| Number | Score | Recommendation | Title | Reasons |
| --- | ---: | --- | --- | --- |
```

## Roadmap

- GitHub API importer
- Policy rules for forbidden files
