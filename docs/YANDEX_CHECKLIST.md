# Sanamaailma — Yandex Games (prepared, NOT submitted)

Archive: `release/sanamaailma-yandex.zip` (index.html in root, 140 files, 18.9 MB zipped / 20.5 MB unpacked; limit 100 MB).
Rebuild: `python3 tools/build_release.py yandex` — adds `/sdk.js`, Yandex adapter, `window.RELEASE=true`; strips test hooks, test badge, noindex and all external links/domains; `shareUrl=null`.
Test: `cd test && node test_release.js` (mock SDK) — ALL PASS.

## Console fields (games.yandex.ru/console, Михаил's account — nothing was created)
| Field | Value |
|---|---|
| Языки | ru (UI Russian; game words Finnish with Russian clues) |
| Архив | `sanamaailma-yandex.zip`, версия 1.0.0 |
| Категории | Головоломки / Словесные (опц. Образовательные) |
| Платформы | Мобильные (портрет) + Десктоп |
| Возраст | 0+ |
| Облачные сохранения | ON (player.setData) |
| Реклама | Fullscreen (every 3rd win, ≥150 s) + Rewarded (🎬 hint, ×2 coins, extra spin) + Sticky banner with «Использовать API для показа sticky-баннера» (shown only after the tutorial) |
| Инапы | нет |
| Лидерборд | technical name **`levels`**, numeric, descending, «Пройдено уровней» |
| Политика | https://pirogovlab.ru/sanamaailma/privacy/ (first upload the ads version `release/privacy_with_ads/index.html`) |

Promo assets (icon 512, cover 800×470, screenshots, video) — not made yet. Texts: `release/store/TEXTS_ru.md`.

## Before submitting
1. `tools/scan_religion.py` → 0; backgrounds without churches/religious symbols.
2. 50 chapter backgrounds are AI-generated photos (allowed, rule 1.23); no music.
3. Draft check with `?debug-mode=16`: loader ready, tutorial, sticky banner only after it, fullscreen/rewarded, sound stops on tab switch.
4. Dictionary: ru.wiktionary, CC BY-SA 4.0 — attribution in credits.
