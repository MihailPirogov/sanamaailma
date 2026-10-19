#!/usr/bin/env python3
"""Finnish lexicon + crossword layout for the Finnish word game «Sanamaailma» (imported by build_game.py).
Sources (in src/, see SOURCES.md):
  ru_fi.jsonl      - Finnish entries of the Russian Wiktionary (ru.wiktionary.org), extracted by Wiktextract / kaikki.org.
                     CC BY-SA 4.0 (+GFDL). Headwords, Russian translations, examples, forms. The ONLY source of shipped glosses/cards.
  lemma_freq.json  - lemma Zipf frequencies: OpenSubtitles 2018 (FrequencyWords) + wordfreq, lemmatised (tools/lemma_freq.py). Level order.
  form_lemma.json  - form -> lemma map of the lemmatiser (rule «not a dictionary form»).
  fiwiki_freq.json - word-form counts from the fi.wikipedia dump (tools/fiwiki_freq.py): only to accept inflected forms as bonus words.
No translation is ever invented: a word without a Russian gloss in the source is a bonus word without translation.
"""
import json, re, random, collections, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = f'{ROOT}/src'; T = f'{ROOT}/tools'; OUT = ROOT
sys.path.insert(0, T)
from religion_filter import religious, offensive
random.seed(42)
freq = json.load(open(f'{S}/fiwiki_freq.json'))
LET = re.compile(r'^[a-zåäö]{3,8}$')
LOAN_LET = re.compile(r'[bcfqwxzšžå]')     # letters found almost only in loanwords (å: Swedish words)
POS_RU = {'noun': 'сущ.', 'verb': 'гл.', 'adj': 'прил.', 'adv': 'нареч.', 'num': 'числ.', 'pron': 'мест.'}
# special-field labels: such words are valid (bonus) but not crossword words
SPECIAL = ('хим.', 'мед.', 'физ.', 'анат.', 'лингв.', 'книжн.', 'диал.', 'матем.', 'истор.', 'техн.', 'биол.', 'астрон.', 'филол.', 'филос.',
           'биохим.', 'геол.', 'спец.', 'физиол.', 'грам.', 'экон.', 'юр.', 'минер.', 'комп.', 'устар.', 'редк.', 'прост.', 'сл.', 'полит.', 'воен.',
           'геометр.', 'информ.', 'полигр.', 'рег.', 'орнитол.', 'ихтиол.', 'энтомол.', 'генет.', 'микол.', 'цитол.', 'палеонт.', 'микробиол.',
           'психиатр.', 'фарм.', 'металл.', 'горн.', 'археол.', 'научн.', 'неол.', 'поэт.', 'высок.', 'нар.', 'фант.', 'эл.', 'текст.', 'геофиз.')
LAB_RE = re.compile(r'^((?:[а-яёА-Я]+\.\s*)+)')
REF_RE = re.compile(r'^(?:см\.|то же,? что|словоформа|форма|мн\. ч\.|прич\. от|деепр\. от|\(?(?:мужское|женское) имя|название буквы)', re.I)
BIBLE_REF = re.compile(r'Biblia|Библи|Евангел|Послани|Книга|Псалт|Откровени|Притч|Исаи|Деяни|Бытие|Исход|Екклез|Песня Песней|1[67]\d\d г\.', re.I)
TOK = re.compile(r'[a-zåäö]+')

TR = {'a': 'а', 'b': 'б', 'c': 'к', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'г', 'h': 'х', 'i': 'и', 'j': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о',
      'p': 'п', 'q': 'к', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'v': 'в', 'w': 'в', 'x': 'кс', 'y': 'ю', 'z': 'з', 'ä': 'я', 'ö': 'ё', 'å': 'о'}
def _skel(t): return re.sub(r'(.)\1+', r'\1', re.sub(r'[ьъйэ]', '', t.replace('ё', 'е').replace('ю', 'у').replace('я', 'а').replace('э', 'е')))
def looks_translit(w, gl):
    """Russian gloss is just the same word in Cyrillic (soul -> соул, ara -> ара, psii -> пси): an international loan, bonus only."""
    a = _skel(''.join(TR.get(c, c) for c in w))
    for g in re.split(r'[;,()]\s*', gl.lower())[:3]:
        b = _skel(g.strip())
        if not b: continue
        if a == b or (len(a) >= 4 and (a[:-1] == b or b[:-1] == a or a[:-1] == b[:-1])): return True
    return False

def split_label(g):
    m = LAB_RE.match(g)
    if not m: return '', g.strip()
    lab = m.group(1).strip()
    if lab in ('см.',): return '', g.strip()
    return lab, g[m.end():].strip()

def clean_gloss(g):
    g = re.sub(r'\s*\([A-Za-z][A-Za-z .]*\)', '', g)        # Latin taxon names in brackets: «лосось (salmo)»
    return re.sub(r'\s+', ' ', g).strip(' ;,')

# ---------- read the Russian Wiktionary ----------
entries = collections.defaultdict(list)    # headword -> list of entry dicts (homonyms)
form_of = {}                               # inflected form -> lemma
NAMES = set()
def form_count(j):
    return sum(freq.get(f['form'], 0) for f in j.get('forms', []) if ' ' not in f.get('form', ''))
for l in open(f'{S}/ru_fi.jsonl', encoding='utf-8'):
    j = json.loads(l); raw = j['word'].strip(); w = raw.lower(); pos = j.get('pos')
    if pos not in POS_RU: continue
    if raw != w or not re.match(r'^[a-zåäö]+$', raw): NAMES.add(w); continue    # proper names, abbreviations, compounds with -/space
    senses = []
    for s in j.get('senses', []):
        if 'form-of' in s.get('tags', []): continue
        gl = [x for x in s.get('glosses', []) if x]
        if not gl: continue
        lab, d = split_label(clean_gloss(gl[0]))
        if not d: continue
        ex = []
        for e in s.get('examples', [])[:4]:
            t = (e.get('text') or '').strip(); tr = (e.get('translation') or '').strip()
            if BIBLE_REF.search(e.get('ref') or ''): continue          # Bible quotations are never shipped
            if t and tr and len(t) < 160: ex.append([t, tr, ''])
        senses.append(dict(lab=lab, d=d, ex=ex))
    if not senses: continue
    extra = []
    for key, name in (('synonyms', 'Синонимы'), ('antonyms', 'Антонимы'), ('derived', 'Производные')):
        it = [x['word'] for x in j.get(key, []) if x.get('word') and not religious(x['word']) and not offensive(x['word'])][:6]
        if it: extra.append(dict(kind=name, items=it))
    e = dict(pos=pos, inf='', senses=senses, extra=extra, f=freq.get(w, 0) * 3 + form_count(j))
    entries[w].append(e)
    for f in j.get('forms', []):
        fw = f.get('form', '').lower()
        if not LET.match(fw) or fw == w: continue
        if fw[:2] != w[:2] or len(fw) < 3: continue     # broken table cells (energia -> «aan»): a real form keeps the stem start
        form_of.setdefault(fw, w)

# ---------- cards ----------
def all_text(es): return ' '.join(s['lab'] + ' ' + s['d'] + ' ' + ' '.join(x[1] for x in s['ex']) for e in es for s in e['senses'])
def resolve_ref(d, depth=0):
    """'см. X' -> X's first gloss"""
    m = re.match(r'^см\.\s*([a-zåäö]+)', d)
    if m and depth < 2 and m.group(1) in entries:
        return resolve_ref(entries[m.group(1)][0]['senses'][0]['d'], depth + 1)
    return d

# ---------- lemma frequencies (tools/lemma_freq.py: OpenSubtitles via FrequencyWords + wordfreq, lemmatised) ----------
LF = json.load(open(f'{S}/lemma_freq.json'))
FORM_LEMMA = json.load(open(f'{S}/form_lemma.json'))
def zipf(w):
    """combined Zipf score: 65 % spoken (subtitles) + 35 % general (wordfreq); 0 if unknown"""
    zs, zw = LF.get(w, (0, 0))
    if zs and zw: return .65 * zs + .35 * zw
    return max(zs, zw) - .3 if (zs or zw) else 0.0
# labels that do not make a word "strange" (common nature / everyday fields)
NEUTRAL_LAB = ('ботан.', 'зоол.', 'кулин.', 'разг.', 'перен.', 'спорт.', 'муз.', 'метеорол.', 'геогр.')
# kept although a secondary sense is religious: only the secular senses are shipped (kaste «роса», munkki «пончик»)
SECULAR_OK = {'kaste', 'munkki'}
# hand-picked: valid words whose first translation is unhelpful for a learner (crossword -> bonus only)
# (found by reviewing the top-1000 list: wrong/secondary first sense in the source, inflected forms, lemmatiser noise)
BONUS_ONLY = {'lama', 'jaa', 'see', 'hai', 'aino', 'hui', 'äh', 'öh', 'hah', 'heh', 'hoh', 'oho', 'ai', 'oi', 'no', 'kas',
              'niittää', 'musta', 'verta', 'venäjän', 'leikata', 'läpi', 'väärä', 'taso', 'usea', 'asu', 'kama', 'lordi', 'laki', 'kirjoita',
              'poikia', 'uusia', 'alusta', 'pelkkä', 'suhde', 'päätös', 'vaate', 'kansio', 'ura', 'munia', 'kukkia', 'lasta', 'maata', 'vähä',
              'pula', 'jakso', 'kate', 'syli', 'pesä', 'kiero', 'siitä', 'tästä', 'siellä', 'täällä', 'pääte', 'elo', 'olo', 'kaira', 'paise', 'taru', 'ote', 'veto', 'tulo', 'erä', 'kai', 'kisa', 'aines'}
# function words (pronouns, quantifiers): never in the first 100 levels, from level 250 on like any word
FUNC_GLOSS = re.compile(r'^(?:я|ты|он|она|оно|мы|вы|они|что|кто|какой|который|каждый|всякий|любой|свой|один,|некий|многие|оба|обе|этот|эта|тот|та|такой|весь|все|всё|сам|никто|ничто|некоторый|несколько|кто-нибудь|что-нибудь|кто-то|что-то)(?![а-яё])')
# not for the very first levels (they stay in the game later): war / weapons / police
EARLY_AVOID = {'sota', 'ase', 'ampua', 'armeija', 'pommi', 'luoti', 'laukaus', 'miekka', 'räjähdys', 'kenraali', 'sotilas', 'taistelu',
               'poliisi', 'isku', 'lyödä', 'vihata', 'syyte', 'tuomio', 'syyttää', 'upseeri', 'majuri', 'eversti', 'hyökätä', 'tuhota', 'varastaa', 'tutkinta'}
RUZ = json.load(open(f'{S}/ru_zipf.json'))
def ruz(g):
    """Russian Zipf frequency of the first word of a translation (wordfreq 'ru'): low = unusual / non-basic translation"""
    m = re.match(r'\(?([а-яё-]+)', (g or '').lower()); return RUZ.get(m.group(1), 0) if m else 0
WHY = collections.Counter()      # why words became bonus-only (report)

UD = {}   # word -> {g: first gloss, loan, card, special, f, z, pos, why}
BANNED = set()
for w, es in entries.items():
    if not LET.match(w): continue
    first_txt = es[0]['senses'][0]['lab'] + ' ' + es[0]['senses'][0]['d']
    if re.search(r'(?:мужское|женское) имя|фамилия|^[А-ЯЁ]', es[0]['senses'][0]['d']): NAMES.add(w); continue   # personal / place names
    if w not in SECULAR_OK and (religious(w, first_txt) or offensive(w, first_txt, es[0]['senses'][0]['lab'])): BANNED.add(w); continue
    hom = []
    for e in es:
        ss = []
        for s in e['senses'][:6]:
            d = resolve_ref(s['d'])
            if religious('', s['lab'] + ' ' + d) or offensive('', d, s['lab']): continue      # drop the sense, keep the word
            ex = [x for x in s['ex'] if not (religious(x[0], x[1]) or offensive('', x[1]) or any(religious(t) or offensive(t) for t in TOK.findall(x[0].lower())))]
            ss.append(dict(n=0, lab=s['lab'], d=d[:200], ex=ex[:2]))
        # most common meaning first: plain senses before labelled ones (перен., устар., спец. …), references last
        ss.sort(key=lambda x: (bool(REF_RE.match(x['d'])), bool(x['lab']) and not any(t in x['lab'] for t in NEUTRAL_LAB)))
        for k, x in enumerate(ss): x['n'] = k + 1
        if ss: hom.append(dict(pos=e['pos'], senses=ss))
    if not hom: BANNED.add(w); continue
    # homonyms: real meanings before "form of …" entries
    hom.sort(key=lambda h: REF_RE.match(h['senses'][0]['d']) is not None)
    first = hom[0]['senses'][0]
    g = first['d']
    loan = bool(LOAN_LET.search(w)) or looks_translit(w, g)
    special = all(any(x in s['lab'] for x in SPECIAL) for h in hom for s in h['senses'][:1])
    ref_only = all(REF_RE.match(s['d']) for h in hom for s in h['senses'])
    z = zipf(w)
    why = ('ref' if ref_only else 'special' if special else 'loan' if loan else
           'manual' if w in BONUS_ONLY else
           'gloss' if re.match(r'^\(|^[a-z]', g) or re.search(r'\((?:в|о|об|у) [а-яё]+', g) or ruz(g) < 2.3 else
           'form' if FORM_LEMMA.get(w, w) != w and FORM_LEMMA[w] in entries and zipf(FORM_LEMMA[w]) > z else
           'rare' if z < 2.2 else '')
    WHY[why or 'grid'] += 1
    gram = ', '.join(sorted({POS_RU[e['pos']] for e in es}))
    ex_by = {}
    for e in es:
        for x in e['extra']:
            lst = ex_by.setdefault(x['kind'], [])
            lst += [i for i in x['items'] if i not in lst]
    extra = [dict(kind=k, items=v[:6]) for k, v in ex_by.items()][:3]
    UD[w] = dict(g=None if ref_only else g, loan=loan, special=special or ref_only, f=sum(e['f'] for e in es), z=z, pos=hom[0]['pos'], why=why,
                 func=hom[0]['pos'] == 'pron' or bool(FUNC_GLOSS.match(g)),
                 card=dict(stress='', gram=gram, hill='', hom=hom, extra=extra, src='wkru'))
UD_COMPLETE = True

def gloss(w):
    if w in UD and UD[w]['g']: return UD[w]['g'][:90], 'ud'
    if w in form_of and form_of[w] in UD and UD[form_of[w]]['g']:
        return ('форма слова ' + form_of[w] + ' — ' + UD[form_of[w]]['g'])[:90], 'ru'
    return None, None

# ---------- lexicon ----------
lex = {}
for w, v in UD.items():
    lex[w] = dict(f=v['z'], b=bool(v['why']) or not v['g'])
for fw, lw in form_of.items():   # attested inflected forms of dictionary words: bonus only
    if fw in lex or lw not in UD or fw in BANNED or freq.get(fw, 0) < 30: continue
    if religious(fw) or offensive(fw): continue
    lex[fw] = dict(f=0, b=True)

def score(w): return lex[w]['f']          # combined Zipf of the lemma (higher = more frequent)
def learn_score(w):
    """order for the crossword: Finnish frequency + a bonus for a plain, common Russian translation (дом, собака > хватка, плоскость)"""
    return score(w) + .6 * (min(ruz(UD[w]['g']), 5.5) - 4.2) if w in UD else score(w)
grid_words = {w for w, e in lex.items() if not e['b']}
bonus_words = set(lex) | grid_words
CORE_POS = ('noun', 'verb', 'adj', 'num')

print('lexicon', len(lex), 'grid', len(grid_words), 'bonus', len(bonus_words), 'banned', len(BANNED), 'why', dict(WHY), file=sys.stderr)
_cc = {}
def can_make(word, pool):
    c = _cc.get(word)
    if c is None: c = _cc[word] = collections.Counter(word)
    return all(pool[k] >= v for k, v in c.items())

# --- crossword layout ---
def layout(words, tries=300):
    best = None
    for t in range(tries):
        ws = sorted(words, key=lambda w: -len(w)) if t == 0 else random.sample(words, len(words))
        if t and random.random() < .5: ws = sorted(ws, key=lambda w: -len(w) + random.random() * 2)
        grid = {}; placed = []
        def fits(w, r, c, d):
            dr, dc = (0, 1) if d == 'h' else (1, 0)
            if (r - dr, c - dc) in grid or (r + dr * len(w), c + dc * len(w)) in grid: return False
            cross = 0
            for i, ch in enumerate(w):
                p = (r + dr * i, c + dc * i)
                if p in grid:
                    if grid[p][0] != ch or grid[p][1] == d: return False
                    cross += 1
                else:
                    n1 = (p[0] + dc, p[1] + dr); n2 = (p[0] - dc, p[1] - dr)
                    if n1 in grid or n2 in grid: return False
            return cross
        def put(w, r, c, d):
            dr, dc = (0, 1) if d == 'h' else (1, 0)
            for i, ch in enumerate(w):
                p = (r + dr * i, c + dc * i)
                grid[p] = (ch, 'x' if p in grid else d)
            placed.append((w, r, c, d))
        put(ws[0], 0, 0, 'h')
        left = ws[1:]; progress = True
        while left and progress:
            progress = False
            for w in list(left):
                opts = []
                for (pr, pc), (ch, pd) in list(grid.items()):
                    if pd == 'x': continue
                    nd = 'v' if pd == 'h' else 'h'
                    for i, wc in enumerate(w):
                        if wc != ch: continue
                        r, c = (pr - i, pc) if nd == 'v' else (pr, pc - i)
                        x = fits(w, r, c, nd)
                        if x: opts.append((x, random.random(), r, c, nd))
                if opts:
                    opts.sort(reverse=True); _, _, r, c, d = opts[0]
                    put(w, r, c, d); left.remove(w); progress = True
        rs = [p[0] for p in grid]; cs = [p[1] for p in grid]
        h = max(rs) - min(rs) + 1; wd = max(cs) - min(cs) + 1
        sc = len(placed) * 100 - abs(h - wd) * 3 - h * wd * 0.5 - max(0, wd - 10) * 50 - max(0, h - 10) * 50
        if best is None or sc > best[0]:
            mr, mc = min(rs), min(cs)
            best = (sc, [(w, r - mr, c - mc, d) for w, r, c, d in placed], h, wd)
        if len(placed) == len(words) and t > 60: break
    return best

