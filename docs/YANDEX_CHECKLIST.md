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

Promo assets: see release/yandex_assets/ (icon 512, cover 800×470, showcase 1560×520, screenshots, video).
- **Horizontal gameplay video (required):** `yandex_assets/gameplay_landscape.mp4`. It is git-ignored; regenerate it with the command below.
  - 27.7 s, H.264 1920×1080 30 fps yuv420p + AAC 48 kHz stereo, 8.1 MB. Yandex limits: MP4, 16:9, height ≥400 px, ≤28 s, ≤100 MB. Contact sheet: `gameplay_landscape_contact_sheet.jpg`.
  - Real gameplay recorded from the release build, with no browser UI and no ads: home → swipes on level 193 → word card → chapter map → daily puzzle → wheel of fortune. The swipe part is sped up 1.25×.
  - The music is an original A-minor kantele-style melody synthesised by `tools/make_trailer.py` (numpy), with no third-party audio. No text overlays, no religious imagery.
  - Re-record: `python3 tools/build_release.py yandex; Xvfb :99 -screen 0 1920x1080x24 & cd test && XGRAB=:99 node trailer_rec.js && python3 ../tools/make_trailer.py`.
 Texts: `release/store/TEXTS_ru.md`.

## Before submitting
1. `tools/scan_religion.py` → 0; backgrounds without churches/religious symbols.
2. 50 chapter backgrounds are AI-generated photos (allowed, rule 1.23); no music.
3. Draft check with `?debug-mode=16`: loader ready, tutorial, sticky banner only after it, fullscreen/rewarded, sound stops on tab switch.
4. Dictionary: ru.wiktionary, CC BY-SA 4.0 — attribution in credits.
