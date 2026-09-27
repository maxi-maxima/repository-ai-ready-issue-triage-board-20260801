# Repository AI-Ready Issue Triage Board

维护者希望 AI Agent 帮忙处理 Issue，但不是每个 Issue 都足够安全、具体、适合交给 Agent。这个 CLI 会按 Agent 可处理度排序，并标记隐私或范围风险。

## 为什么现在值得做

GitHub 和开发者社区正在推动 issue-to-PR Agent、自动分诊和多 Agent 编码团队。真正的瓶颈不是启动更多 Agent，而是选择正确的任务。

## 安装与运行

```bash
python -m repository_ai_ready_issue_triage_board_20260801.cli examples/issues.json
python -m repository_ai_ready_issue_triage_board_20260801.cli examples/issues.json --format json
python -m repository_ai_ready_issue_triage_board_20260801.cli examples/issues.json --format markdown
python -m repository_ai_ready_issue_triage_board_20260801.cli examples/issues.json --forbid-label security --forbid-label legal
python -m unittest discover -s tests
```

可重复传入 `--forbid-label`，让匹配标签的 Issue 无论分数多高都保留给人工处理。标签按不区分大小写的完整名称匹配。

## 示例

```csv
number,score,recommendation,title,reasons
12,95,delegate_to_agent,Crash on save,has reproduction clues; has concrete evidence; label suggests delegation
```

Markdown 输出适合粘贴到项目看板或 Issue 评论：

```markdown
| Number | Score | Recommendation | Title | Reasons |
| --- | ---: | --- | --- | --- |
```

## 路线图

- GitHub API 导入器
- forbidden files 策略规则
