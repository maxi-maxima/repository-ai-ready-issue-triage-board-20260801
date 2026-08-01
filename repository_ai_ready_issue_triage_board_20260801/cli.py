import argparse
import csv
import json
import re
import sys


def score_issue(issue):
    text = (issue.get('title', '') + '\n' + issue.get('body', '')).lower()
    score = 50
    reasons = []
    if re.search(r'\b(repro|steps|expected|actual|fixture|test)\b', text):
        score += 20
        reasons.append('has reproduction clues')
    if re.search(r'\b(file|path|line|stack trace|traceback|screenshot)\b', text):
        score += 15
        reasons.append('has concrete evidence')
    if re.search(r'\b(password|token|secret|private|credential|payment|pii)\b', text):
        score -= 25
        reasons.append('privacy/security sensitive')
    if re.search(r'\b(refactor everything|rewrite|vague|sometimes|flaky)\b', text):
        score -= 15
        reasons.append('ambiguous scope')
    labels = [str(x).lower() for x in issue.get('labels', [])]
    if any('good first' in x or 'agent' in x for x in labels):
        score += 10
        reasons.append('label suggests delegation')
    return max(0, min(100, score)), reasons


def recommendation(score, reasons):
    reason_text = '; '.join(reasons)
    if score >= 80 and 'privacy/security sensitive' not in reason_text and 'ambiguous scope' not in reason_text:
        return 'delegate_to_agent'
    if score >= 55:
        return 'needs_maintainer_review'
    return 'keep_human_owned'


def load(path):
    with open(path, encoding='utf-8', newline='') as handle:
        data = json.load(handle)
    return data if isinstance(data, list) else data.get('issues', [])


def build_rows(issues):
    rows = []
    for issue in issues:
        score, reasons = score_issue(issue)
        rows.append({
            'number': issue.get('number'),
            'title': issue.get('title', ''),
            'score': score,
            'recommendation': recommendation(score, reasons),
            'reasons': '; '.join(reasons),
        })
    rows.sort(key=lambda r: (-r['score'], r['number'] or 0))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description='Build an AI-agent-ready triage board from issue JSON.')
    ap.add_argument('issues_json')
    ap.add_argument('--format', choices=['csv', 'json'], default='csv', help='output format')
    ns = ap.parse_args(argv)
    rows = build_rows(load(ns.issues_json))
    if ns.format == 'json':
        print(json.dumps({'issues': rows}, indent=2))
        return
    w = csv.DictWriter(sys.stdout, fieldnames=['number', 'score', 'recommendation', 'title', 'reasons'])
    w.writeheader()
    w.writerows(rows)


if __name__ == '__main__':
    main()
