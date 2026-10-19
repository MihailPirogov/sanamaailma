<p align="center"><img src="store/icon_512.png" width="128" alt="Sanamaailma"></p>

<h1 align="center">Sanamaailma — мир финских слов</h1>

<p align="center">
<img src="https://img.shields.io/badge/Android-7.0%2B-3ddc84?logo=android&logoColor=white" alt="Android 7.0+">
<img src="https://img.shields.io/badge/HTML5-offline-e34f26?logo=html5&logoColor=white" alt="HTML5">
<a href="LICENSE"><img src="https://img.shields.io/badge/code-MIT-informational" alt="MIT"></a>
<img src="https://img.shields.io/badge/data-CC%20BY--SA%204.0-lightgrey" alt="CC BY-SA 4.0">
<a href="https://pirogovlab.ru/sanamaailma-igra/"><img src="https://img.shields.io/badge/site-pirogovlab.ru-0b2545" alt="site"></a>
</p>

<p align="center"><img src="store/feature_graphic_1024x500.png" width="720" alt="Sanamaailma — мир финских слов"></p>

**RU** · [EN](#english)

Словесная головоломка на финском языке: соединяйте буквы на круге, составляйте финские слова и заполняйте кроссворд. 1000 уровней в 50 главах, карточка с переводом на русский для каждого слова. Работает без интернета.

<!-- PLACEHOLDER store badges: add RuStore / Google Play / Yandex Games links when the listings are live -->
**Играть в браузере:** https://pirogovlab.ru/sanamaailma/ · **Страница игры:** https://pirogovlab.ru/sanamaailma-igra/ · **Скачать APK:** https://pirogovlab.ru/sanamaailma/sanamaailma.apk

## Возможности
- **1000 уровней в 50 главах** (Озеро, Лес, Сауна, Белая ночь, Северное сияние, Лапландия, Шхеры…), у каждой главы свой фотофон финской природы.
- Буквы **Ä Ö** прямо на колесе; порядок слов — по частоте в живой речи.
- **Карточки слов**: перевод, значения и примеры; «Мой словарь» с выученными словами.
- Задача дня, слово дня, ежедневная награда, задания, колесо удачи, достижения, бонусные слова и копилка.
- Интерактивное обучение; подсказки (буква, слово, перемешать).
- Платформы: веб, Android (WebView + Yandex Mobile Ads), Яндекс Игры (SDK v2).

## Скриншоты
<p>
<img src="store/screenshots/phone_2_game.png" width="180"> <img src="store/screenshots/phone_3_card.png" width="180"> <img src="store/screenshots/phone_4_map.png" width="180"> <img src="store/screenshots/phone_7_home.png" width="180">
</p>

## Данные
- Слова, переводы и примеры: финские статьи русского Викисловаря (ru.wiktionary.org) через Wiktextract / kaikki.org. Лицензия **CC BY-SA 4.0**, поэтому `data/` распространяется под той же лицензией.
- Частоты слов: FrequencyWords (Hermit Dave, OpenSubtitles 2018) и wordfreq (Robyn Speer и др.), CC BY-SA 4.0; в игру попадает только порядок уровней.
- Религиозная и ненормативная лексика исключена (`tools/religion_filter.py`, проверка `tools/scan_religion.py`).
- Подробнее: [SOURCES.md](SOURCES.md). Исходные дампы в репозиторий не входят; их скачивает `tools/fetch_sources.sh`.

## Сборка
```bash
tools/rebuild_all.sh                     # данные + проверки + тесты (нужны дампы в src/)
cd test && npm i && node test.js && node test_tutorial.js && node dup_swipe.js
python3 tools/build_release.py yandex    # архив для Яндекс Игр (+ node test_release.js)
tools/build_android.sh                   # подписанные APK/AAB (JDK 17, Android SDK 36, Gradle 8.13)
```
Ключи подписи хранятся **вне репозитория**: `release/keys/keystore.properties` (в .gitignore), с полями `storeFile`, `storePassword`, `keyAlias`, `keyPassword`. Без них соберётся только debug-APK (`tools/build_android.sh debug`).
Рекламные блоки задаются в `android/app/src/main/res/values/ads.xml`.

Структура:
- `index.html`, `css/`, `js/`, `fonts/`: игра;
- `data/`: уровни и карточки;
- `img/bg/`: фоны глав;
- `android/`: оболочка;
- `tools/`: сборка данных, фонов, иконок, релизов;
- `test/`: Playwright-тесты;
- `design/`: промо-графика;
- `docs/`: чек-листы релиза;
- `store/`: тексты и скриншоты для магазинов.

## Лицензии
- Код: MIT ([LICENSE](LICENSE)).
- Словарные данные в `data/`: CC BY-SA 4.0 (© авторы Викисловаря).
- Фоны глав (`img/bg/`) — изображения, сгенерированные ИИ. Иконка и графика © PirogovLab.
- Шрифты Manrope и Unbounded: SIL OFL 1.1 (`fonts/`).

## Автор
Проект [PirogovLab](https://pirogovlab.ru) — Михаил Пирогов.

---

## English

**Sanamaailma** (“World of Words”) is a word puzzle in the Finnish language: connect letters on the wheel, build Finnish words and fill the crossword. It has 1000 levels in 50 chapters and a word card with a Russian translation for every word. Works offline. Web, Android (WebView) and Yandex Games builds. Code: MIT; dictionary data: CC BY-SA 4.0 (Wiktionary).
