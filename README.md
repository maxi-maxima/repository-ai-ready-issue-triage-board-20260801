# Repository AI-Ready Issue Triage Board

Maintainers want AI agents to help, but not every issue is safe or specific enough to delegate. This CLI ranks issues by agent readiness and flags privacy or scope risks.

## Why now

GitHub and developer communities are pushing issue-to-PR agents, automated triage, and multi-agent coding teams. The bottleneck is choosing the right work, not merely starting more agents.

## Install and run

```bash
python -m repository_ai_ready_issue_triage_board_20260801.cli examples/issues.json
python -m unittest discover -s tests
```

## Example

```csv
number,score,title,reasons
12,95,Crash on save,has reproduction clues; has concrete evidence; label suggests delegation
```

## Roadmap

- GitHub API importer
- Markdown project-board output
- Policy rules for forbidden labels and files
