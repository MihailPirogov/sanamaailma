#!/usr/bin/env python3
"""Print levels with words + translations and a difficulty summary per 100 levels. Usage: report_levels.py [ids...]"""
import json, os, sys, statistics
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(f'{R}/data/levels.js', encoding='utf-8').read(); D = json.loads(s[s.index('=') + 1:s.rstrip().rindex(';')])
Z = json.load(open(f'{R}/src/lemma_freq.json'))
def z(w): a, b = Z.get(w, (0, 0)); return .6 * a + .4 * b if a and b else max(a, b)
ids = [int(x) for x in sys.argv[1:]] or list(range(1, 11))
for i in ids:
    lv = D['levels'][i - 1]
    print(f"{lv['id']:>4} [{lv['l'].upper()}] " + '; '.join(f"{x[0]} — {lv['g'][x[0]][0]}" for x in lv['w']))
for k in range(0, len(D['levels']), 100):
    L = D['levels'][k:k + 100]
    print(f"levels {k+1}-{k+100}: letters {statistics.mean(len(l['l']) for l in L):.1f}, words {statistics.mean(len(l['w']) for l in L):.1f}, "
          f"mean zipf {statistics.mean(z(x[0]) for l in L for x in l['w']):.2f}, min zipf {min(z(x[0]) for l in L for x in l['w']):.2f}")
