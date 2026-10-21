#!/bin/bash
# Stage the PUBLIC web build into dist_web/ (mirrors /mut-tunya/: canonical + OG, indexable, no test badge).
# Deploy (owner's OK only): tar to root@95.142.37.63:/var/www/www-root/data/www/pirogovlab.ru/sanamaailma/ && chown -R www-root:www-root
set -e
cd "$(dirname "$0")/.."
rm -rf dist_web && mkdir dist_web
cp -r index.html css js data fonts img privacy dist_web/
rm -f dist_web/js/adapters/android.js dist_web/js/adapters/yandex.js
[ -f release/sanamaailma.apk ] && cp release/sanamaailma.apk dist_web/sanamaailma.apk
python3 - <<'PY'
import re
p='dist_web/index.html'; s=open(p,encoding='utf-8').read()
head=('<link rel="canonical" href="https://pirogovlab.ru/sanamaailma/">\n'
'<meta property="og:type" content="website"><meta property="og:site_name" content="Pirogov Lab"><meta property="og:locale" content="ru_RU">\n'
'<meta property="og:title" content="Sanamaailma — словесная игра на финском языке"><meta property="og:description" content="Соединяйте буквы, составляйте финские слова и заполняйте кроссворд. 1000 уровней, карточки слов с переводом на русский."><meta property="og:url" content="https://pirogovlab.ru/sanamaailma/">\n'
'<meta property="og:image" content="https://pirogovlab.ru/sanamaailma-igra/img/og-sanamaailma.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">\n'
'<meta name="twitter:card" content="summary_large_image">\n</head>')
assert 'name="robots"' not in s and 'testBadge' not in s and 'canonical' not in s
s=s.replace('</head>',head,1)
import re as _re
m=_re.search(r'<script src="js/platform\.js(\?v=[^"]*)?"></script>', s); assert m
v=m.group(1) or ''
s=s.replace(m.group(0), m.group(0)+'\n<script src="js/webads_config.js'+v+'"></script>\n<script src="js/adapters/web.js'+v+'"></script>',1)
open(p,'w',encoding='utf-8').write(s)
p='dist_web/privacy/index.html'; s=open(p,encoding='utf-8').read()
s2=s.replace('<meta name="robots" content="noindex,nofollow">','<link rel="canonical" href="https://pirogovlab.ru/sanamaailma/privacy/">\n<meta name="robots" content="index, follow">')
assert s2!=s and 'noindex' not in s2; open(p,'w',encoding='utf-8').write(s2)
PY
! grep -rl 'noindex\|testBadge' dist_web --include=*.html
du -sh dist_web
