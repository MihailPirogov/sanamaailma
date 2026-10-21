#!/usr/bin/env python3
# NOTE (21.10.2026): one-shot generator, already applied. Live pages were since edited on the server (Google Play link, RSYa cookie note, «Как играть»); never re-upload its output — always patch the CURRENT server files.
"""Stage the public pages for «Sanamaailma» on pirogovlab.ru (ported from tatar-wow/tools/stage_site.py).
Input: read-only copies of the live pages in site_stage/live/ (the «Сүз дөньясы» landing/blog post are used as templates only).
Output: site_stage/out/ — new folders sanamaailma-igra/, en/sanamaailma-igra/, blog/DATE-sanamaailma/, en/blog/…, blog/media/sanamaailma*.{jpg,webp},
and patched copies of index.html, en/index.html, blog/index.html, en/blog/index.html, blog/rss.xml, en/blog/rss.xml, sitemap.xml.
The web game itself stays the noindex test at /sanamaailma/ (not added to the sitemap)."""
import re, os, html, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = ROOT + '/site_stage/live/'; O = ROOT + '/site_stage/out/'
DATE = sys.argv[1] if len(sys.argv) > 1 else '2026-10-19'
Y, M, D = DATE.split('-'); MRU = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'][int(M)-1]
MEN = ['January','February','March','April','May','June','July','August','September','October','November','December'][int(M)-1]
DRU = f'{int(D)} {MRU} {Y}'; DEN = f'{MEN} {int(D)}, {Y}'
dt = datetime.date(int(Y), int(M), int(D)); RFC = dt.strftime('%a, %d %b %Y') + ' 15:00:00 +0300'
SLUG = f'{DATE}-sanamaailma'; VER = '1.0.0'
APK = '/sanamaailma/sanamaailma.apk'; SIZE_RU = '26 МБ'; SIZE_EN = '26 MB'
GAME = '/sanamaailma/'; PRIV = '/sanamaailma/privacy/'
RU_P = 'https://pirogovlab.ru/sanamaailma-igra/'; EN_P = 'https://pirogovlab.ru/en/sanamaailma-igra/'
OG = 'https://pirogovlab.ru/sanamaailma-igra/img/og-sanamaailma.jpg'
IMG = '/sanamaailma-igra/img/'
e = html.escape
def rd(p): return open(L + p, encoding='utf-8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(O + p), exist_ok=True); open(O + p, 'w', encoding='utf-8').write(s)
def sub1(pat, rep, s, flags=0):
    n, k = re.subn(pat, rep, s, count=1, flags=flags); assert k == 1, pat; return n

def head(s, title, desc, canon, ogt, ogd, ogimg, ru, en):
    s = sub1(r'<title>.*?</title>', f'<title>{e(title)}</title>', s)
    s = sub1(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', s)
    s = sub1(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{canon}">', s)
    s = sub1(r'<link rel="alternate" hreflang="ru" href="[^"]*">', f'<link rel="alternate" hreflang="ru" href="{ru}">', s)
    s = sub1(r'<link rel="alternate" hreflang="en" href="[^"]*">', f'<link rel="alternate" hreflang="en" href="{en}">', s)
    s = sub1(r'<link rel="alternate" hreflang="x-default" href="[^"]*">', f'<link rel="alternate" hreflang="x-default" href="{ru}">', s)
    s = sub1(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{e(ogt)}">', s)
    s = sub1(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{e(ogd)}">', s)
    s = sub1(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{canon}">', s)
    s = sub1(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{ogimg}">', s)
    s = sub1(r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{ogimg}">', s)
    return s

GP_SVG = '<svg viewBox="0 0 24 26" aria-hidden="true" width="26" height="28"><path fill="#00d7fe" d="M1 .6 13.4 13 1 25.4C.6 25.2.4 24.7.4 24.1V1.9C.4 1.3.6.8 1 .6z"/><path fill="#ffce00" d="m17.5 8.9 4.3 2.4c1.3.8 1.3 2 0 2.8l-4.3 2.4L13.4 13z"/><path fill="#ff3a44" d="M17.5 17.1 13.4 13 1 25.4c.5.4 1.2.4 2 0z"/><path fill="#00f076" d="M17.5 8.9 3 .6C2.2.2 1.5.2 1 .6L13.4 13z"/></svg>'
def stores(lang):
    t = (lambda ru, en: ru if lang == 'ru' else en)
    return ('<!-- PLACEHOLDER stores: set href and remove "hidden" when each listing is live -->\n      <div class="stores-row">'
      f'<a class="store rs" href="#rustore" rel="noopener" hidden><i>R</i><span><small>{t("Скачать в","Get it on")}</small><b>RuStore</b></span></a>'
      f'<a class="store gp" href="#google-play" rel="noopener" hidden>{GP_SVG}<span><small>{t("Доступно в","Get it on")}</small><b>Google Play</b></span></a>'
      f'<a class="store yg" href="#yandex-games" rel="noopener" hidden><i>Я</i><span><small>{t("Играть в","Play on")}</small><b>{t("Яндекс Играх","Yandex Games")}</b></span></a></div>')
SH = {'ru': [('game','Кроссворд и круг с буквами'),('card','Карточка слова с переводом'),('map','Карта: 50 глав'),('daily','Задача дня'),('spin','Колесо удачи'),('home','Главный экран'),('tutorial','Обучение при первом запуске')],
      'en': [('game','Crossword and the letter wheel'),('card','Word card with translation'),('map','Map: 50 chapters'),('daily','Daily puzzle'),('spin','Fortune wheel'),('home','Home screen'),('tutorial','First-launch tutorial')]}
def gal(lang): return '<div class="gal">' + ''.join(f'<figure class="shot"><img src="{IMG}screen-{k}.webp" width="540" height="960" loading="lazy" alt="{c}"><figcaption>{c}</figcaption></figure>' for k, c in SH[lang]) + '</div>'

def landing(lang):
    s = rd(('en/' if lang == 'en' else '') + 'suz-donyasy-igra/index.html')
    pre, post = s[:s.index('<main')], s[s.index('</main>') + len('</main>'):]
    assert 'class="tilt"' not in pre or True
    if lang == 'ru':
        pre = head(pre, 'Sanamaailma — словесная игра на финском языке | Pirogov Lab',
          'Sanamaailma («Мир слов») — бесплатная словесная головоломка: составляйте финские слова из букв, 1000 уровней в 50 главах, перевод каждого слова на русский. Игра в браузере и на Android, скоро в RuStore, Google Play и Яндекс Играх.',
          RU_P, 'Sanamaailma — словесная игра на финском языке', 'Соединяйте буквы, составляйте финские слова и заполняйте кроссворд. 1000 уровней, карточки слов с переводом, задача дня и колесо удачи.', OG, RU_P, EN_P)
        pre = pre.replace('<span class="crumb">Сүз дөньясы</span>', '<span class="crumb">Sanamaailma</span>').replace('/suz-donyasy-igra/', '/sanamaailma-igra/')
        main = f'''<main class="wrap">
  <header>
    <div>
      <img class="applogo" src="{IMG}logo.webp" width="256" height="256" alt="Sanamaailma">
      <p class="eyebrow"><span>Suomen kieli · Android · Браузер</span></p>
      <h1>Sanamaailma — мир финских слов</h1>
      <p class="lead">Словесная головоломка на <b>финском языке</b>: соединяйте буквы на круге, составляйте слова и заполняйте кроссворд. <b>1000 уровней</b>, а у каждого слова — карточка с переводом на русский.</p>
      <div class="dl"><a class="btn" href="{GAME}">▶ Играть в браузере</a><a class="btn ghost" href="{APK}" download>⬇ Скачать APK ({VER}, {SIZE_RU})</a></div>
      {stores('ru')}
      <div class="meta"><span class="pill">Версия {VER}</span><span class="pill">{DRU}</span><span class="pill">Android 7.0+</span><span class="pill">Бесплатно</span></div>
    </div>
    <figure class="hero-app"><div class="tilt"><img src="{IMG}screen-game.webp" width="540" height="960" alt="Sanamaailma — уровень с кроссвордом и кругом букв" fetchpriority="high"></div></figure>
  </header>
  <hr class="rule" style="margin-top:1rem">
  <section aria-labelledby="f"><h2 id="f">Возможности</h2><div class="card"><ul style="padding-left:1.2rem;margin:0">
    <li><b>1000 уровней в 50 главах</b> — Озеро, Лес, Сауна, Белая ночь, Северное сияние, Лапландия, Шхеры, Маяк…; у каждой главы свой фотофон финской природы</li>
    <li><b>Буквы Ä и Ö</b> — прямо на колесе, ничего набирать не нужно</li>
    <li><b>Карточки слов</b> — нажмите на найденное слово: перевод на русский, значения и примеры</li>
    <li><b>«Мой словарь»</b> — все выученные слова в одном месте; бонусные слова попадают в копилку</li>
    <li><b>Каждый день</b> — задача дня, слово дня, ежедневная награда, задания, колесо удачи и достижения</li>
    <li>Подсказки: открыть букву, открыть слово, перемешать; короткое обучение при первом запуске; работает <b>без интернета</b></li>
  </ul></div></section>
  <section aria-labelledby="s"><h2 id="s">Скриншоты</h2><figure class="shot" style="margin-bottom:1.5rem"><img src="{IMG}feature-graphic.webp" width="1024" height="500" loading="lazy" alt="Sanamaailma — мир финских слов"></figure>
  {gal('ru')}
  <div class="wide"><figure class="shot"><img src="{IMG}desktop-game.webp" width="1280" height="720" loading="lazy" alt="Версия для компьютера"><figcaption>В браузере на компьютере</figcaption></figure><figure class="shot"><img src="{IMG}desktop-card.webp" width="1280" height="720" loading="lazy" alt="Карточка слова на компьютере"><figcaption>Карточка слова</figcaption></figure></div></section>
  <section aria-labelledby="i"><h2 id="i">Где играть</h2><div class="card"><p style="margin:0">Прямо сейчас — <a href="{GAME}">в браузере</a> на телефоне или компьютере (прогресс сохраняется на устройстве) или на Android: скачайте <a href="{APK}" download>sanamaailma.apk</a> ({VER}, {SIZE_RU}), откройте файл и разрешите установку из этого источника. Скоро Sanamaailma появится в RuStore, Google Play и Яндекс Играх.</p></div></section>
  <section aria-labelledby="src"><h2 id="src">Словарь</h2><div class="card"><ul class="src" style="padding-left:1.2rem;margin:0"><li>Слова, переводы и примеры — финские статьи <a href="https://ru.wiktionary.org" target="_blank" rel="noopener">Викисловаря</a> (CC BY-SA 4.0; данные Wiktextract / kaikki.org)</li><li>Частоты слов — FrequencyWords (OpenSubtitles) и wordfreq (CC BY-SA 4.0)</li></ul>
  <p class="note">В мобильных версиях есть ненавязчивая реклама (после обучения, между уровнями и по желанию — за подсказку). <a href="{PRIV}">Политика конфиденциальности</a>.</p></div></section>
  <aside class="callout" role="note" style="margin-top:3rem"><div class="callout-ico" aria-hidden="true">✦</div><p><b>Kiitos!</b> · Проект лаборатории <a href="https://pirogovlab.ru">PirogovLab</a>. Нашли ошибку в слове или переводе? Напишите в <a href="/contacts/">Telegram</a>.</p></aside>
</main>'''
        post = post.replace('/suz-donyasy/privacy/', PRIV)
        wr('sanamaailma-igra/index.html', pre + main + post)
    else:
        pre = head(pre, 'Sanamaailma — a word game in the Finnish language | Pirogov Lab',
          'Sanamaailma (“World of Words”) is a free word puzzle: build Finnish words from letters, 1000 levels in 50 chapters, a Russian translation for every word. Play in the browser or on Android; RuStore, Google Play and Yandex Games coming soon.',
          EN_P, 'Sanamaailma — a word game in the Finnish language', 'Connect letters, build Finnish words and fill the crossword. 1000 levels, word cards with translations, a daily puzzle and a fortune wheel.', OG, RU_P, EN_P)
        pre = pre.replace('<span class="crumb">Süz Dönyası</span>', '<span class="crumb">Sanamaailma</span>').replace('/suz-donyasy-igra/', '/sanamaailma-igra/')
        main = f'''<main class="wrap">
  <header>
    <div>
      <img class="applogo" src="{IMG}logo.webp" width="256" height="256" alt="Sanamaailma">
      <p class="eyebrow"><span>Finnish language · Android · Browser</span></p>
      <h1>Sanamaailma — the world of Finnish words</h1>
      <p class="lead">A word puzzle in the <b>Finnish language</b>: connect letters on the wheel, build words and fill the crossword. <b>1000 levels</b>, and every word has a card with its Russian translation.</p>
      <div class="dl"><a class="btn" href="{GAME}" hreflang="ru">▶ Play in the browser</a><a class="btn ghost" href="{APK}" download>⬇ Download APK ({VER}, {SIZE_EN})</a></div>
      {stores('en')}
      <div class="meta"><span class="pill">Version {VER}</span><span class="pill">{DEN}</span><span class="pill">Android 7.0+</span><span class="pill">Free</span></div>
    </div>
    <figure class="hero-app"><div class="tilt"><img src="{IMG}screen-game.webp" width="540" height="960" alt="Sanamaailma — a level with the crossword and the letter wheel" fetchpriority="high"></div></figure>
  </header>
  <hr class="rule" style="margin-top:1rem">
  <section aria-labelledby="f"><h2 id="f">Features</h2><div class="card"><ul style="padding-left:1.2rem;margin:0">
    <li><b>1000 levels in 50 chapters</b> (Lake, Forest, Sauna, White Night, Northern Lights, Lapland, Skerries, Lighthouse…), each with its own photo of Finnish nature</li>
    <li><b>The letters Ä and Ö</b> right on the wheel, no typing needed</li>
    <li><b>Word cards</b>: tap a found word to see its Russian translation, meanings and examples</li>
    <li><b>“My dictionary”</b>: every word you have learned; bonus words go into a jar</li>
    <li><b>Every day</b>: a daily puzzle, a word of the day, a daily reward, quests, a fortune wheel and achievements</li>
    <li>Hints: reveal a letter, reveal a word, shuffle; a short tutorial; works <b>offline</b>; the interface is in Russian</li>
  </ul></div></section>
  <section aria-labelledby="s"><h2 id="s">Screenshots</h2><figure class="shot" style="margin-bottom:1.5rem"><img src="{IMG}feature-graphic.webp" width="1024" height="500" loading="lazy" alt="Sanamaailma"></figure>
  {gal('en')}
  <div class="wide"><figure class="shot"><img src="{IMG}desktop-game.webp" width="1280" height="720" loading="lazy" alt="Desktop browser version"><figcaption>In a desktop browser</figcaption></figure><figure class="shot"><img src="{IMG}desktop-card.webp" width="1280" height="720" loading="lazy" alt="A word card on desktop"><figcaption>A word card</figcaption></figure></div></section>
  <section aria-labelledby="i"><h2 id="i">Where to play</h2><div class="card"><p style="margin:0">Right now: <a href="{GAME}" hreflang="ru">in the browser</a> on a phone or computer (progress is saved on the device), or on Android: download <a href="{APK}" download>sanamaailma.apk</a> ({VER}, {SIZE_EN}), open it and allow installs from this source. RuStore, Google Play and Yandex Games are coming soon.</p></div></section>
  <section aria-labelledby="src"><h2 id="src">Dictionary</h2><div class="card"><ul class="src" style="padding-left:1.2rem;margin:0"><li>Words, translations and examples: Finnish entries of the Russian <a href="https://ru.wiktionary.org" target="_blank" rel="noopener">Wiktionary</a> (CC BY-SA 4.0; Wiktextract / kaikki.org data)</li><li>Word frequencies: FrequencyWords (OpenSubtitles) and wordfreq (CC BY-SA 4.0)</li></ul>
  <p class="note">The mobile versions show unobtrusive ads (after the tutorial, between levels and, if you choose, for a hint). <a href="{PRIV}" hreflang="ru">Privacy policy</a>.</p></div></section>
  <aside class="callout" role="note" style="margin-top:3rem"><div class="callout-ico" aria-hidden="true">✦</div><p>A <a href="https://pirogovlab.ru/en/">PirogovLab</a> project. Found a mistake in a word or translation? Message me on <a href="/en/contacts/">Telegram</a>.</p></aside>
</main>'''
        post = post.replace('/suz-donyasy/privacy/', PRIV)
        wr('en/sanamaailma-igra/index.html', pre + main + post)

def blogpost(lang):
    s = rd(('en/' if lang == 'en' else '') + 'blog/2026-10-19-suz-donyasy/index.html')
    pre, post = s[:s.index('<main')], s[s.index('</main>') + len('</main>'):]
    ru_u = f'https://pirogovlab.ru/blog/{SLUG}/'; en_u = f'https://pirogovlab.ru/en/blog/{SLUG}/'; img = 'https://pirogovlab.ru/blog/media/sanamaailma.jpg'
    if lang == 'ru':
        T = '«Sanamaailma»: словесная игра на финском языке'
        DS = 'Сделал «Sanamaailma» — словесную головоломку на финском: 1000 уровней, перевод каждого слова на русский, задача дня и колесо удачи. Играть можно в браузере и на Android, скоро — RuStore, Google Play и Яндекс Игры.'
        pre = head(pre, T + ' | Pirogov Lab', DS, ru_u, T, DS, img, ru_u, en_u)
        pre = pre.replace('/blog/2026-10-19-suz-donyasy/', f'/blog/{SLUG}/')
        main = f'''<main class="wrap">
<article class="full">
  <p class="eyebrow"><a href="/blog/">Микроблог</a></p>
  <h1>{T}</h1>
  <time class="date" datetime="{DATE}T15:00:00+03:00">{DRU}</time>
  <figure class="media"><img src="/blog/media/sanamaailma.jpg" width="1200" height="630" alt="{T}"></figure>
  <div class="body">
<p>Новая словесная игра — на этот раз на <b>финском</b>, дальнем родственнике марийского: <b>«Sanamaailma»</b> («Мир слов»). Соединяете буквы на круге, составляете финские слова и заполняете ими кроссворд.</p>
<h2>Что внутри</h2>
<ul>
<li><b>1000 уровней в 50 главах</b>: Озеро, Лес, Сауна, Белая ночь, Северное сияние, Лапландия, Шхеры… У каждой главы своя фотография финской природы — озёра, шхеры, полярная ночь.</li>
<li>Буквы <b>Ä и Ö</b> прямо на колесе.</li>
<li><b>Карточки слов</b>: нажмите на найденное слово — перевод на русский, значения и примеры из Викисловаря. Выученные слова собираются в «Мой словарь».</li>
<li><b>Каждый день</b> — задача дня, слово дня, ежедневная награда, задания, колесо удачи и достижения.</li>
<li>Подсказки, бонусные слова, короткое обучение при первом запуске. Работает <b>без интернета</b>.</li>
</ul>
<p>Слова и переводы взяты из открытого Викисловаря (CC BY-SA 4.0), порядок уровней — по частоте слов в живой речи: сначала sana, iso, suuri, потом посложнее. Играть можно <b>прямо в браузере</b> на телефоне и компьютере или на Android (APK), скоро Sanamaailma появится в RuStore, Google Play и Яндекс Играх.</p>
<p>Нашли ошибку в слове или переводе? Напишите мне в <a href="/contacts/">Telegram</a> — буду исправлять. Kiitos!</p>
  </div>
  <div class="stores"><a class="btn" href="{GAME}">▶ Играть в браузере</a></div>
  <div class="meta"><span class="pill">Версия {VER}</span><a class="pill" href="https://pirogovlab.ru{APK}" download>⬇ Android: скачать APK ({SIZE_RU})</a><a class="pill" href="/sanamaailma-igra/">Страница игры</a><span class="pill">Бесплатно</span></div>
  <a class="proj" href="/sanamaailma-igra/"><img src="{IMG}kartochka-sanamaailma.webp" width="480" height="320" alt=""><div><b>Sanamaailma</b><span>Страница игры: возможности, скриншоты, где играть</span></div><span class="go" aria-hidden="true">→</span></a>
  <a class="backlink" href="/blog/">← Все записи</a>
</article>
</main>'''
        wr(f'blog/{SLUG}/index.html', pre + main + post)
    else:
        T = 'Sanamaailma: a word game in the Finnish language'
        DS = 'I made Sanamaailma, a word puzzle in Finnish: 1000 levels, a Russian translation for every word, a daily puzzle and a fortune wheel. Play in the browser or on Android; RuStore, Google Play and Yandex Games coming soon.'
        pre = head(pre, T + ' | Pirogov Lab', DS, en_u, T, DS, img, ru_u, en_u)
        pre = pre.replace('/blog/2026-10-19-suz-donyasy/', f'/blog/{SLUG}/')
        main = f'''<main class="wrap">
<article class="full">
  <p class="eyebrow"><a href="/en/blog/">Microblog</a></p>
  <h1>{T}</h1>
  <time class="date" datetime="{DATE}T15:00:00+03:00">{DEN}</time>
  <figure class="media"><img src="/blog/media/sanamaailma.jpg" width="1200" height="630" alt="{T}"></figure>
  <div class="body">
<p>A new word game, this time in <b>Finnish</b>, a distant relative of Mari: <b>Sanamaailma</b> (“World of Words”). Connect letters on the wheel, build Finnish words and fill the crossword with them.</p>
<h2>What's inside</h2>
<ul>
<li><b>1000 levels in 50 chapters</b>, each with its own photo of Finnish nature: lakes, skerries, white nights and the northern lights.</li>
<li>The letters <b>Ä and Ö</b> right on the wheel.</li>
<li><b>Word cards</b>: tap a found word to see its Russian translation, meanings and examples from Wiktionary. Learned words go into “My dictionary”.</li>
<li><b>Every day</b>: a daily puzzle, a word of the day, a daily reward, quests, a fortune wheel and achievements.</li>
<li>Hints, bonus words and a short tutorial on first launch. Works <b>offline</b>.</li>
</ul>
<p>Words and translations come from the open Wiktionary (CC BY-SA 4.0); levels follow word frequency in everyday speech. You can <b>play right in the browser</b> or on Android (APK) now; RuStore, Google Play and Yandex Games are coming soon. The interface is in Russian.</p>
<p>Found a mistake in a word or translation? Message me on <a href="/en/contacts/">Telegram</a>. Kiitos!</p>
  </div>
  <div class="stores"><a class="btn" href="{GAME}" hreflang="ru">▶ Play in the browser</a></div>
  <div class="meta"><span class="pill">Version {VER}</span><a class="pill" href="https://pirogovlab.ru{APK}" download>⬇ Android: download APK ({SIZE_EN})</a><a class="pill" href="/en/sanamaailma-igra/">Game page</a><span class="pill">Free</span></div>
  <a class="proj" href="/en/sanamaailma-igra/"><img src="{IMG}kartochka-sanamaailma.webp" width="480" height="320" alt=""><div><b>Sanamaailma</b><span>Game page: features, screenshots, where to play</span></div><span class="go" aria-hidden="true">→</span></a>
  <a class="backlink" href="/en/blog/">← All posts</a>
</article>
</main>'''
        wr(f'en/blog/{SLUG}/index.html', pre + main + post)

def patch(rel, fn):
    s = rd(rel); assert 'sanamaailma-igra' not in s, rel + ' already has Sanamaailma'; n = fn(s); assert n != s, rel; wr(rel, n)
def feed_add(s, mb, cap):
    i = s.index('<a class="mbf"'); s = s[:i] + mb + s[i:]
    items = list(re.finditer(r'      <a class="mbf" href="[^"]*".*?</a>\n', s, re.S))
    if len(items) > cap: last = items[-1]; s = s[:last.start()] + s[last.end():]
    return s
def home_ru(s):
    n0 = len(re.findall(r'<a class="mbf"', s))
    s = feed_add(s, f'<a class="mbf" href="/blog/{SLUG}/"><img src="/blog/media/sanamaailma-thumb.webp" width="960" height="540" alt=""><div><time datetime="{DATE}">{DRU}</time><b>«Sanamaailma»: словесная игра на финском</b><span>Соединяйте буквы, составляйте финские слова и заполняйте кроссворд: 1000 уровней и перевод каждого слова — играть в браузере</span></div></a>\n      ', n0)
    pj = f'<a class="proj" href="/sanamaailma-igra/"><img src="{IMG}kartochka-sanamaailma.webp" width="480" height="320" alt="Sanamaailma — словесная игра на финском языке"><div><b>Sanamaailma — мир финских слов</b><span>Словесная головоломка на финском: 1000 уровней и перевод каждого слова — игра в браузере и на Android</span></div><span class="go" aria-hidden="true">→</span></a>\n  '
    i = s.index('<a class="proj"'); return s[:i] + pj + s[i:]
def home_en(s):
    n0 = len(re.findall(r'<a class="mbf"', s))
    s = feed_add(s, f'<a class="mbf" href="/en/blog/{SLUG}/"><img src="/blog/media/sanamaailma-thumb.webp" width="960" height="540" alt=""><div><time datetime="{DATE}">{DEN}</time><b>Sanamaailma: a word game in Finnish</b><span>Connect letters, build Finnish words and fill the crossword: 1000 levels and a translation for every word — play in the browser</span></div></a>\n      ', n0)
    pj = f'<a class="proj" href="/en/sanamaailma-igra/"><img src="{IMG}kartochka-sanamaailma.webp" width="480" height="320" alt="Sanamaailma — a word game in the Finnish language"><div><b>Sanamaailma — the world of Finnish words</b><span>A word puzzle in Finnish: 1000 levels and a translation for every word — browser and Android</span></div><span class="go" aria-hidden="true">→</span></a>\n  '
    i = s.index('<a class="proj"'); return s[:i] + pj + s[i:]
def blog_idx(lang):
    def f(s):
        if lang == 'ru':
            a = f'''  <article class="card post">
    <time class="date" datetime="{DATE}T15:00:00+03:00">{DRU}</time>
    <h2><a href="/blog/{SLUG}/">«Sanamaailma»: словесная игра на финском языке</a></h2>
    <figure class="media"><img src="/blog/media/sanamaailma.jpg" width="1200" height="630" alt="Sanamaailma — мир финских слов" loading="lazy"></figure>
    <p>Словесная головоломка на финском: соединяйте буквы, составляйте слова и заполняйте кроссворд. 1000 уровней в 50 главах, перевод каждого слова на русский, задача дня и колесо удачи. Играть можно в браузере и на Android, скоро — RuStore, Google Play и Яндекс Игры.</p>
    <a class="more" href="/blog/{SLUG}/">Читать полностью →</a>
  </article>
'''
        else:
            a = f'''  <article class="card post">
    <time class="date" datetime="{DATE}T15:00:00+03:00">{DEN}</time>
    <h2><a href="/en/blog/{SLUG}/">Sanamaailma: a word game in the Finnish language</a></h2>
    <figure class="media"><img src="/blog/media/sanamaailma.jpg" width="1200" height="630" alt="Sanamaailma — the world of Finnish words" loading="lazy"></figure>
    <p>A word puzzle in Finnish: connect letters, build words and fill the crossword. 1000 levels in 50 chapters, a Russian translation for every word, a daily puzzle and a fortune wheel. Play in the browser or on Android; RuStore, Google Play and Yandex Games coming soon.</p>
    <a class="more" href="/en/blog/{SLUG}/">Read more →</a>
  </article>
'''
        assert '  <div class="feed">\n' in s
        return s.replace('  <div class="feed">\n', '  <div class="feed">\n' + a, 1)
    return f
def rss(lang):
    def f(s):
        base = f'https://pirogovlab.ru/blog/{SLUG}/' if lang == 'ru' else f'https://pirogovlab.ru/en/blog/{SLUG}/'
        t = '«Sanamaailma»: словесная игра на финском языке' if lang == 'ru' else 'Sanamaailma: a word game in the Finnish language'
        d = ('Словесная головоломка на финском: 1000 уровней, перевод каждого слова, задача дня и колесо удачи. Игра в браузере и на Android.' if lang == 'ru'
             else 'A word puzzle in Finnish: 1000 levels, a translation for every word, a daily puzzle and a fortune wheel. Browser and Android.')
        item = f'    <item>\n      <title>{e(t)}</title>\n      <link>{base}</link>\n      <guid isPermaLink="true">{base}</guid>\n      <pubDate>{RFC}</pubDate>\n      <description>{e(d)}</description>\n    </item>\n'
        s = re.sub(r'<lastBuildDate>.*?</lastBuildDate>', f'<lastBuildDate>{RFC}</lastBuildDate>', s, count=1)
        i = s.index('    <item>'); return s[:i] + item + s[i:]
    return f
def sitemap(s):
    add = ''.join(f'  <url><loc>https://pirogovlab.ru/{u}</loc><lastmod>{DATE}</lastmod></url>\n' for u in
        ['sanamaailma-igra/', 'en/sanamaailma-igra/', f'blog/{SLUG}/', f'en/blog/{SLUG}/'])
    for u in ['', 'en/', 'blog/', 'en/blog/']:
        s = re.sub(rf'(<url><loc>https://pirogovlab.ru/{re.escape(u)}</loc><lastmod>)[^<]*', rf'\g<1>{DATE}', s)
    return s.replace('</urlset>', add + '</urlset>')

if __name__ == '__main__':
    landing('ru'); landing('en'); blogpost('ru'); blogpost('en')
    patch('index.html', home_ru); patch('en/index.html', home_en)
    patch('blog/index.html', blog_idx('ru')); patch('en/blog/index.html', blog_idx('en'))
    patch('blog/rss.xml', rss('ru')); patch('en/blog/rss.xml', rss('en')); patch('sitemap.xml', sitemap)
    print('staged ->', O, 'slug', SLUG)
