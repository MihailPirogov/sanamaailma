#!/usr/bin/env python3
"""Lemma frequencies for Finnish from two open sources (run with the build venv: .venv/bin/python tools/lemma_freq.py):
  1. FrequencyWords 2018 fi_full (Hermit Dave, OpenSubtitles 2018 — spoken / everyday language), content CC BY-SA 4.0
     https://github.com/hermitdave/FrequencyWords  -> src/fw_fi_full.txt (word forms + counts)
  2. wordfreq 3.x Finnish list (Robyn Speer et al.; Wikipedia, subtitles, news, books, web, Reddit, Twitter — general language), data CC BY-SA 4.0
     https://github.com/rspeer/wordfreq
Word forms are lemmatised with simplemma (MIT; build-time tool only, nothing of it is shipped), falling back to the declension
tables of ru.wiktionary (src/ru_fi.jsonl). Output src/lemma_freq.json: {lemma: [zipf_subtitles, zipf_wordfreq, lemma_lemmatizer_disagrees]}
plus src/form_lemma.json (frequent form -> lemma) for the 'not a dictionary form' rule. Only numbers are kept."""
import json, math, os, re, collections, sys
import simplemma, wordfreq
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); S = f'{R}/src'
TOK = re.compile(r'^[a-zåäö]+$')
form_of = {}; tables = collections.defaultdict(set); head_pos = collections.defaultdict(set)
for l in open(f'{S}/ru_fi.jsonl', encoding='utf-8'):
    j = json.loads(l); w = j['word']
    if any('form-of' not in x.get('tags', []) and not re.match(r'^(?:форма|словоформа)', (x.get('glosses') or [''])[0]) for x in j.get('senses', [])):
        head_pos[w].add(j.get('pos'))       # real headwords only (ru.wiktionary also has «форма глагола …» entries such as olen, on)
    for f in j.get('forms', []):
        fw = re.sub(r'\(.*?\)', '', f.get('form', '')).strip().lower()
        if TOK.match(fw) and fw != w: form_of.setdefault(fw, w); tables[fw].add(w)
cache = {}
def lemma(form):
    """simplemma, cross-checked with ru.wiktionary headwords / declension tables (simplemma alone maps e.g. työ -> sinä, alle -> energia)"""
    if form in cache: return cache[form]
    L = simplemma.lemmatize(form, lang='fi').lower()
    if not TOK.match(L): L = form
    plaus = L != form and L[:2] == form[:2]
    verbL = 'verb' in head_pos.get(L, ()) and L[:3] == form[:3] if len(L) > 4 else 'verb' in head_pos.get(L, ()) and L[:2] == form[:2]
    if 'verb' in head_pos.get(form, ()): lm = form                                  # kuulla is a verb, not «on the moon»
    elif plaus and (L in tables.get(form, ()) or verbL): lm = L                      # lasta -> lapsi, tuli -> tulla, voi -> voida
    elif form in head_pos: lm = form                                                # työ, musta, tee stay themselves
    elif form in form_of: lm = form_of[form]
    else: lm = L if plaus else form
    cache[form] = lm; return lm
def aggregate(pairs, total):
    agg = collections.Counter()
    for form, n in pairs: agg[lemma(form)] += n
    return {k: math.log10(v / total * 1e9) for k, v in agg.items() if v > 0}
subs = []; tot = 0
for line in open(f'{S}/fw_fi_full.txt', encoding='utf-8'):
    p = line.split()
    if len(p) != 2: continue
    w, n = p[0].lower(), int(p[1]); tot += n
    if n >= 3 and TOK.match(w): subs.append((w, n))
zs = aggregate(subs, tot)
wf = wordfreq.get_frequency_dict('fi')
zw = aggregate([(w, p * 1e9) for w, p in wf.items() if TOK.match(w)], 1e9)
out = {}
for k in set(zs) | set(zw):
    out[k] = [round(zs.get(k, 0), 3), round(zw.get(k, 0), 3)]
json.dump(out, open(f'{S}/lemma_freq.json', 'w'), ensure_ascii=False)
fl = {f: l for f, l in cache.items() if f != l}
json.dump(fl, open(f'{S}/form_lemma.json', 'w'), ensure_ascii=False)
print('subtitle forms', len(subs), 'tokens', tot, 'lemmas', len(out), 'form->lemma', len(fl), file=sys.stderr)
# Russian frequency of the first word of each first translation (wordfreq 'ru'): «strange / non-basic translation» signal
G = {}
for l in open(f'{S}/ru_fi.jsonl', encoding='utf-8'):
    j = json.loads(l)
    for x in j.get('senses', []):
        g = (x.get('glosses') or [''])[0]
        g = re.sub(r'^(?:[а-яё]+\.\s*)+', '', g).strip()
        m = re.match(r'\(?([а-яё-]+)', g.lower())
        if m and m.group(1) not in G: G[m.group(1)] = round(wordfreq.zipf_frequency(m.group(1), 'ru'), 2)
json.dump(G, open(f'{S}/ru_zipf.json', 'w'), ensure_ascii=False)
print('ru gloss words', len(G), file=sys.stderr)
