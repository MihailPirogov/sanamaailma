# Sanamaailma («Мир слов») — финская игра в слова (рабочее название)
Пакет на будущее: `ru.pirogovlab.sanamaailma`. Проект PirogovLab (Михаил Пирогов).
Движок — от «Сүз дөньясы» (/workspace/tatar-wow, не изменялся): колесо букв + кроссворд; **дизайн свой** (скандинавский): палитра navy / ice / snow / spruce + rowan/cloudberry,
шрифты Manrope + Unbounded (OFL, встроены в css/fonts.css — работает из file://), круглые «камешки» букв на тёмном стеклянном диске со снежинкой,
плоские ледяные клетки с переворотом (flip) при отгадывании, домашний экран с карточкой главы, круглый док иконок (свои SVG line-icons), карта глав — «открытки»,
светлые «снежные» панели, снежинки вместо конфетти, 21 процедурная сцена финской природы (js/art.js).

Открыть `index.html` (офлайн) или `python3 -m http.server` в папке.

- `tools/fetch_sources.sh` — скачать источники в `src/` (SOURCES.md).
- `tools/lexicon.py` — финский лексикон из ru.wiktionary: только строчные нарицательные слова 3–8 букв (a–z, å, ä, ö); имена собственные, аббревиатуры, фамилии,
  названия букв, слова с иностранными буквами (b c f q w x z š ž å) и «транслитерации» (soul → соул) — только бонусные; спец. термины (хим., мед., орнитол. …) — бонусные.
- `tools/religion_filter.py` — стоп-лист религии/мифологии/магии/загробного мира (fi + рус. перевод), мат/грубое/18+/алкоголь/смерть/насилие; значения и примеры с такими словами удаляются из карточек.
- `tools/build_game.py 1000 20` → `data/levels.js` (`window.TT_DATA`: 1000 уровней, 50 глав по 20, 366 задач дня, 366 слов дня) + `data/cards/c<код>.js`.
  Примерно каждый 3-й уровень — с ä/ö (иначе гармония гласных вытесняет их из колеса).
- `tools/validate_levels.py` — независимая проверка: каждое слово кроссворда и бонус собираются из букв колеса, нет конфликтов клеток, кроссворд связный, у всех слов есть перевод.
- `tools/scan_religion.py` — проверка готовых данных на религиозное/грубое → 0 совпадений.
- `tools/rebuild_all.sh` — сборка + проверки + headless-тесты (без деплоя!).
- Тесты: `cd test && SHOTS=../screens node test.js && SHOTS=../screens/tutorial node test_tutorial.js` (playwright-core + /usr/bin/google-chrome).
- Сравнение с татарской версией: `screens/compare/*.jpg`. Фоны: `cd test && node shots_art.js`.
- Музыки нет. Веб-версия (pirogovlab.ru) — без рекламы и SDK (`?adsim=1` — только симуляция).
- Релизные сборки с рекламой (порт из tatar-wow, не опубликованы):
  - `python3 tools/build_release.py yandex` → `release/sanamaailma-yandex.zip` (Яндекс Игры SDK: fullscreen, rewarded, sticky-баннер, облако, лидерборд `levels`), тест `cd test && node test_release.js`;
  - `tools/build_android.sh debug` → `release/sanamaailma-debug.apk` (WebView + Yandex Mobile Ads 8.6.0), тест `node test_android_www.js`;
  - ID рекламных блоков — только в `android/app/src/main/res/values/ads.xml` (приложение РСЯ 20244945: R-M-20244945-1/2/3, в тестовом режиме до добавления ссылки на магазин; debug/signtest — демо-блоки);
  - чек-листы: `release/ANDROID_CHECKLIST.md`, `release/YANDEX_CHECKLIST.md`, тексты `release/store/TEXTS_ru.md`.

## Web ads (public site build only)
`tools/stage_public.sh` adds `js/webads_config.js` + `js/adapters/web.js` (Yandex.RTB loader `yandex.ru/ads/system/context.js`, `yaContextCb`, `Ya.Context.AdvManager.render`):
sticky banner (`renderTo`), interstitial (`type: 'fullscreen'`), and rewards via a SEPARATE fullscreen block (RSYa web has no rewarded format; reward only if it was shown).
Show points/caps are the shared ones in `js/app.js`. Placeholder IDs = ads off. Yandex Games / Android builds never include these files (guard in `tools/build_release.py`). Test: `node test/test_webads.js` (mocked Ya.Context).
