import argparse, json, re, csv, sys

def score_issue(issue):
    text=(issue.get('title','')+'\n'+issue.get('body','')).lower()
    score=50
    reasons=[]
    if re.search(r'\b(repro|steps|expected|actual|fixture|test)\b', text): score+=20; reasons.append('has reproduction clues')
    if re.search(r'\b(file|path|line|stack trace|traceback|screenshot)\b', text): score+=15; reasons.append('has concrete evidence')
    if re.search(r'\b(password|token|secret|private|credential|payment|pii)\b', text): score-=25; reasons.append('privacy/security sensitive')
    if re.search(r'\b(refactor everything|rewrite|vague|sometimes|flaky)\b', text): score-=15; reasons.append('ambiguous scope')
    labels=[str(x).lower() for x in issue.get('labels',[])]
    if any('good first' in x or 'agent' in x for x in labels): score+=10; reasons.append('label suggests delegation')
    return max(0,min(100,score)), reasons

def load(path):
    data=json.loads(open(path,encoding='utf-8').read())
    return data if isinstance(data,list) else data.get('issues',[])

def main(argv=None):
    ap=argparse.ArgumentParser(description='Build an AI-agent-ready triage board from issue JSON.')
    ap.add_argument('issues_json')
    ns=ap.parse_args(argv)
    rows=[]
    for issue in load(ns.issues_json):
        score,reasons=score_issue(issue)
        rows.append({'number':issue.get('number'),'title':issue.get('title',''),'score':score,'reasons':'; '.join(reasons)})
    rows.sort(key=lambda r:(-r['score'], r['number'] or 0))
    w=csv.DictWriter(sys.stdout, fieldnames=['number','score','title','reasons'])
    w.writeheader(); w.writerows(rows)
if __name__=='__main__': main()
