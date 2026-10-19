#!/usr/bin/env python3
"""Independent validator for data/levels.js: every level is solvable, every crossword word (and bonus word) can be built from the
letters of the wheel (multiset), crossword cells are consistent and connected, all letters are from the Finnish alphabet,
words are 3-8 letters, every crossword word has a Russian translation, chapters are contiguous. Exit 1 on any error."""
import json, os, re, sys, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(ROOT, 'data/levels.js'), encoding='utf-8').read()
D = json.loads(s[s.index('=') + 1:s.rstrip().rindex(';')])
ALPHA = re.compile(r'^[a-zåäö]+$')
err = []; stats = collections.Counter()
def fits(w, letters): return not (collections.Counter(w) - collections.Counter(letters))
for lv in D['levels'] + D['daily']:
    L = lv['l']; lid = lv['id']; grid = {}
    if not ALPHA.match(L): err.append(f'{lid}: wheel letters {L!r} outside the Finnish alphabet')
    if not 4 <= len(L) <= 8: err.append(f'{lid}: wheel size {len(L)}')
    ws = [x[0] for x in lv['w']]
    if len(set(ws)) != len(ws): err.append(f'{lid}: duplicate crossword word')
    if len(ws) < 2: err.append(f'{lid}: only {len(ws)} words')
    if not any(len(w) == len(L) for w in ws): stats['no_full_word'] += 1
    for w, r, c, d in lv['w']:
        if not (3 <= len(w) <= 8 and ALPHA.match(w)): err.append(f'{lid}: bad word {w}')
        if not fits(w, L): err.append(f'{lid}: {w} cannot be built from {L}')
        if w not in lv['g']: err.append(f'{lid}: {w} has no translation')
        for i, ch in enumerate(w):
            k = (r, c + i) if d == 'h' else (r + i, c)
            if k in grid and grid[k] != ch: err.append(f'{lid}: clash at {k} in {w}')
            grid[k] = ch
        if r < 0 or c < 0 or (d == 'h' and c + len(w) > lv['c']) or (d == 'v' and r + len(w) > lv['r']): err.append(f'{lid}: {w} outside {lv["r"]}x{lv["c"]}')
    # connectivity of the crossword (all words reachable through shared cells)
    cells = [set(((r, c + i) if d == 'h' else (r + i, c)) for i in range(len(w))) for w, r, c, d in lv['w']]
    seen = {0}; todo = [0]
    while todo:
        a = todo.pop()
        for b in range(len(cells)):
            if b not in seen and cells[a] & cells[b]: seen.add(b); todo.append(b)
    if len(seen) != len(cells): err.append(f'{lid}: crossword not connected')
    for b in lv['b']:
        if not fits(b, L): err.append(f'{lid}: bonus {b} cannot be built from {L}')
        if b in ws: err.append(f'{lid}: bonus {b} also in crossword')
    stats['levels'] += 1; stats['words'] += len(ws)
    if re.search('[äöå]', L): stats['with_äöå'] += 1
ch = D['chapters']
if ch[0]['start'] != 1 or ch[-1]['end'] != len(D['levels']) or any(ch[i]['start'] != ch[i - 1]['end'] + 1 for i in range(1, len(ch))): err.append('chapters not contiguous')
print('validated', dict(stats), 'levels', len(D['levels']), 'daily', len(D['daily']), 'chapters', len(ch), '-> errors', len(err))
for e in err[:30]: print('  ', e)
sys.exit(1 if err else 0)
