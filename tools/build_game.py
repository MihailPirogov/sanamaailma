#!/usr/bin/env python3
"""Build all game data for the Finnish word game «Sanamaailma» (working title, «Мир слов»):
   data/levels.js  - window.TT_DATA = {chapters, levels, daily, wotd, meta}
   data/cards/cXXXX.js - word cards chunked by first letter (lazy-loaded)
Usage: build_game.py [N_LEVELS=800] [CHAPTER_SIZE=16]
"""
import sys, os, json, random, itertools, collections, re, time
sys.path.insert(0, os.path.dirname(__file__))
from lexicon import *          # lex, grid_words, bonus_words, score, gloss, layout, UD, UD_COMPLETE, OUT, S
from religion_filter import religious, offensive
# no religious words in crosswords, daily puzzles, bonus words or word of the day
RELIGIOUS = {w for w in set(grid_words) | set(bonus_words) if religious(w, gloss(w)[0] or '') or offensive(w, gloss(w)[0] or '')}
grid_words = {w for w in grid_words if w not in RELIGIOUS}
bonus_words = {w for w in bonus_words if w not in RELIGIOUS}
print('religious stop-list: excluded', len(RELIGIOUS), 'words', file=sys.stderr)
random.seed(7)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 800
CH = int(sys.argv[2]) if len(sys.argv) > 2 else 16
D = f'{OUT}/data'; os.makedirs(f'{D}/cards', exist_ok=True)
t0 = time.time()

FRONT = re.compile('[äö]')
def sig(w): return ''.join(sorted(w))
by_sig = collections.defaultdict(list)
for w in grid_words: by_sig[sig(w)].append(w)
bonus_by_sig = collections.defaultdict(list)
for w in bonus_words: bonus_by_sig[sig(w)].append(w)

def sub_sigs(base):
    s = sorted(base); out = set()
    for k in range(3, len(s) + 1):
        for comb in itertools.combinations(range(len(s)), k):
            out.add(''.join(s[i] for i in comb))
    return out

def has_gloss(w): return gloss(w)[0] is not None


# ---- chapters ----
CHAPTERS = [  # (finnish, russian, theme) - Finnish nature, places, seasons and everyday culture (nothing religious or mythological)
 ('Järvi', 'Озеро', 'lake'), ('Metsä', 'Лес', 'forest'), ('Ranta', 'Берег', 'shore'), ('Mökki', 'Домик у озера', 'cabin'),
 ('Sauna', 'Сауна', 'cabin'), ('Saari', 'Остров', 'archipelago'), ('Koivu', 'Берёза', 'birch'), ('Mustikka', 'Черника', 'forest'),
 ('Kesä', 'Лето', 'summer'), ('Kesäyö', 'Белая ночь', 'midnight'), ('Syksy', 'Осень', 'autumn'), ('Ruska', 'Золотая осень', 'autumn'),
 ('Talvi', 'Зима', 'winter'), ('Lumi', 'Снег', 'winter'), ('Kaamos', 'Полярная ночь', 'aurora'), ('Revontulet', 'Северное сияние', 'aurora'),
 ('Kevät', 'Весна', 'spring'), ('Koski', 'Порог', 'river'), ('Suo', 'Болото', 'bog'), ('Tunturi', 'Сопка', 'fell'),
 ('Lappi', 'Лапландия', 'fell'), ('Poro', 'Олень', 'fell'), ('Karhu', 'Медведь', 'forest'), ('Joutsen', 'Лебедь', 'lake'),
 ('Meri', 'Море', 'sea'), ('Majakka', 'Маяк', 'sea'), ('Satama', 'Гавань', 'harbor'), ('Saaristo', 'Шхеры', 'archipelago'),
 ('Kaupunki', 'Город', 'city'), ('Tori', 'Рыночная площадь', 'city'), ('Kylä', 'Деревня', 'village'), ('Pelto', 'Поле', 'field'),
 ('Tie', 'Дорога', 'field'), ('Silta', 'Мост', 'river'), ('Juna', 'Поезд', 'winter'), ('Kahvi', 'Кофе', 'cabin'),
 ('Leipä', 'Хлеб', 'village'), ('Kala', 'Рыба', 'lake'), ('Sieni', 'Гриб', 'autumn'), ('Kukka', 'Цветок', 'spring'),
 ('Tuuli', 'Ветер', 'sea'), ('Sade', 'Дождь', 'river'), ('Aurinko', 'Солнце', 'summer'), ('Kuu', 'Луна', 'midnight'),
 ('Tähti', 'Звезда', 'aurora'), ('Jää', 'Лёд', 'winter'), ('Hiihto', 'Лыжи', 'fell'), ('Laulu', 'Песня', 'village'),
 ('Koti', 'Дом', 'cabin'), ('Maailma', 'Мир', 'lake'),
]
# ---- vocabulary threshold: frequency rank of crossword words grows with the level ----
ORDER = sorted(grid_words, key=lambda w: -learn_score(w))
RANK = {w: i for i, w in enumerate(ORDER)}
CORE = [w for w in ORDER if UD[w]['pos'] in CORE_POS and not UD[w]['func']]           # nouns, verbs, adjectives, numerals
CORE_RANK = {w: i for i, w in enumerate(CORE)}
NG = len(ORDER)
def cap(i):
    """levels 1-100: only the 1000 most frequent everyday nouns/verbs/adjectives/numerals; then the threshold widens smoothly"""
    return int(1400 + (NG - 1400) * ((i - 100) / max(1, N - 100)) ** 1.5)
def allowed(w, i):
    if i < 100: return CORE_RANK.get(w, 1 << 30) < (450 if i < 30 else 1000) and not UD[w]['func'] and w not in EARLY_AVOID
    if i < 250 and UD[w]['func']: return False                       # pronouns / function words only after level 250
    return RANK[w] < cap(i)

bases = []                                                          # (base, sub-words sorted by frequency)
seen = set()
for base in ORDER:
    if not 4 <= len(base) <= 8 or sig(base) in seen: continue
    seen.add(sig(base)); ss = sub_sigs(base)
    subs = sorted({w for s_ in ss for w in by_sig.get(s_, [])}, key=lambda w: RANK[w])
    if len(subs) >= 3: bases.append(dict(base=base, subs=subs, ss=ss, L=len(base)))
by_len = collections.defaultdict(list)
for c in bases: by_len[c['L']].append(c)
print('bases', {L: len(v) for L, v in sorted(by_len.items())}, file=sys.stderr)

def length_for(i, n):
    x = i / max(1, n - 1)            # 0..1 smooth curve
    for L, edge in ((4, .03), (5, .16), (6, .40), (7, .72), (8, 1.01)):
        if x < edge: return L
    return 8
def max_words(L, i): return 3 if i < 20 else min(L + (1 if i > 500 and L >= 5 else 0), 9)

used = set(); USE = collections.Counter(); featured = set()
def theme_word(i):
    if i >= N: return None
    tw = CHAPTERS[(i // CH) % len(CHAPTERS)][0].lower()
    return tw if tw in grid_words and (i // CH) not in featured else None
def pick(c, i, mx):
    words = [w for w in c['subs'] if w != c['base'] and allowed(w, i)]
    if len(words) < 2: return None
    words.sort(key=lambda w: -(learn_score(w) - .45 * USE[w]))        # frequent first, but vary words already used often
    return [c['base']] + words[:mx - 1]
def take(i, L, rnd=False):
    tw = theme_word(i)
    for LL in [L, L - 1, L + 1, L - 2, L + 2]:
        if not 4 <= LL <= 8: continue
        mx = max_words(LL, i); cands = []
        for c in by_len.get(LL, []):
            if sig(c['base']) in used or not allowed(c['base'], i): continue
            ch = pick(c, i, mx)
            if not ch: continue
            q = sum(learn_score(w) for w in ch) / len(ch) - .3 * sum(USE[w] for w in ch) / len(ch) + .02 * len(ch)
            cands.append((q, c, ch))
        if not cands: continue
        if tw:                                                   # link a level of the chapter to its theme word (Järvi, Kala, Sauna …)
            th = [x for x in cands if tw in x[2]]
            if th: featured.add(i // CH); cands = th
        if i % 3 == 1 and i >= 3:                                # Finnish feel: every third level with ä/ö
            fv = [x for x in cands if FRONT.search(x[1]['base'])]
            if len(fv) >= 3: cands = fv
        cands.sort(key=lambda x: -x[0])
        q, c, ch = random.choice(cands[:6]) if rnd else cands[0] if i < 40 else random.choice(cands[:3])
        used.add(sig(c['base']))
        for w in ch: USE[w] += 1
        return c, ch
    return None, None

def make_level(c, chosen, lid):
    _, placed, h, wd = layout(chosen, tries=160)
    placed_words = {p[0] for p in placed}
    bonus = sorted({w for s_ in c['ss'] for w in bonus_by_sig.get(s_, [])} - placed_words)
    letters = list(c['base']); random.shuffle(letters)
    while ''.join(letters) == c['base'] and len(set(letters)) > 1: random.shuffle(letters)
    gl = {}
    for w in list(placed_words) + bonus:
        g, lang = gloss(w)
        if g: gl[w] = [g, lang]
    return dict(id=lid, l=''.join(letters), r=h, c=wd, w=[[w, r, cc, d] for w, r, cc, d in placed], b=bonus, g=gl)

SRC_CODE = {'wkru': 'wkru'}
levels = []
for i in range(N):
    c, ch = take(i, length_for(i, N))
    if not c: print('pools exhausted at', i, file=sys.stderr); break
    levels.append(make_level(c, ch, i + 1))
    if i % 100 == 99: print('levels', i + 1, round(time.time() - t0), 's', file=sys.stderr)
daily = []
for i in range(366):
    c, ch = take(500 + i, 5 if i % 3 else 6, rnd=True)
    if not c: break
    daily.append(make_level(c, ch, 'd%d' % (i + 1)))
print('daily', len(daily), file=sys.stderr)

chapters = []
for k in range(0, len(levels), CH):
    m, r, th = CHAPTERS[(k // CH) % len(CHAPTERS)]
    n = k // CH + 1
    if k // CH >= len(CHAPTERS): m, r = f'{m} {k // CH // len(CHAPTERS) + 1}', f'{r} {k // CH // len(CHAPTERS) + 1}'
    chapters.append(dict(n=n, tt=m, ru=r, theme=th, start=k + 1, end=min(k + CH, len(levels))))

# ---- word of the day pool ----
def good_card(w):
    if w not in UD or UD[w]['loan'] or not UD[w]['g']: return False
    return any(x['ex'] for h in UD[w]['card']['hom'] for x in h['senses']) and not UD[w]['special']
in_game = {x[0] for lv in levels for x in lv['w']}
wotd = sorted([w for w in in_game if good_card(w) and len(w) >= 3], key=lambda w: -score(w))[:600]
random.shuffle(wotd); wotd = wotd[:366]
if len(wotd) < 366:   # not enough cards with examples: top up with well-known words that have a translation card
    more = sorted([w for w in in_game if w in UD and UD[w]['g'] and not UD[w]['loan'] and not UD[w]['special'] and w not in wotd and len(w) >= 3], key=lambda w: -score(w))
    wotd += more[:366 - len(wotd)]

# ---- cards (chunked) ----
def compact(card):
    homs = []
    for h in card['hom']:
        ss = []
        for x in h['senses'][:5]:
            if not x['d'] and not x['ex']: continue
            ss.append(dict(n=x['n'], l=x['lab'], d=x['d'][:200], e=[[e[0][:160], e[1][:160], e[2][:30]] for e in x['ex'][:2]]))
        if ss: homs.append(ss)
    ex = [dict(k=e['kind'], i=e['items'][:6]) for e in card.get('extra', []) if e['items']][:3]
    return dict(s=card.get('stress', ''), g=card.get('gram', ''), h=card.get('hill', ''), m=homs[:3], x=ex, src=SRC_CODE.get(card.get('src', ''), 'wkru'))
words_needed = set(in_game) | set(wotd) | {w for lv in levels + daily for w in lv['b']} | {x[0] for lv in daily for x in lv['w']}
chunks = collections.defaultdict(dict)
for w in words_needed:
    if w in UD: chunks[ord(w[0])][w] = compact(UD[w]['card'])
for f in os.listdir(f'{D}/cards'): os.remove(f'{D}/cards/{f}')
for k, v in chunks.items():
    with open(f'{D}/cards/c{k}.js', 'w') as f:
        f.write('TT_CARDS_PUSH(' + json.dumps(v, ensure_ascii=False, separators=(',', ':')) + ');\n')

grid_total = sum(len(lv['w']) for lv in levels)
grid_gl = sum(1 for lv in levels for x in lv['w'] if x[0] in lv['g'])
grid_ud = sum(1 for lv in levels for x in lv['w'] if lv['g'].get(x[0], ['', ''])[1] == 'ud')
meta = dict(built=time.strftime('%Y-%m-%d %H:%M'), full_dictionary=UD_COMPLETE, levels=len(levels), chapters=len(chapters), daily=len(daily),
            grid_words=grid_total, grid_with_translation=grid_gl, grid_from_dictionary=grid_ud, cards=sum(len(v) for v in chunks.values()),
            card_chunks=sorted(chunks))
data = dict(meta=meta, chapters=chapters, levels=levels, daily=daily, wotd=wotd)
with open(f'{D}/levels.js', 'w') as f:
    f.write('window.TT_DATA=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
json.dump(meta, open(f'{D}/meta.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(meta, ensure_ascii=False), file=sys.stderr)
print('time', round(time.time() - t0), 's', file=sys.stderr)
