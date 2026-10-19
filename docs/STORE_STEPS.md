# Sanamaailma 1.0.0 — план публикации (RuStore, Google Play, Яндекс Игры, РСЯ)

**Ничего не отправлено.** Способ у всех игр PirogovLab — **через браузерные консоли** (API/сервис-аккаунтов для Play или RuStore на боксе нет, у других игр тоже не использовались). Платежей не нужно: все аккаунты уже есть.

| | |
|---|---|
| Название | **Sanamaailma** (запасное: «Sanamaailma — финские слова») |
| Пакет | `ru.pirogovlab.sanamaailma` · 1.0.0 (versionCode 1) · minSdk 24 · targetSdk 36 |
| Реклама | Yandex Mobile Ads, приложение РСЯ **20244945** (R-M-20244945-1/2/3), сейчас «Тестовый режим» |
| Подпись | собственный ключ Sanamaailma, SHA-256 `94:F6:BB:EF:E2:49:DC:1A:BA:04:FA:3A:19:AE:6B:73:5A:E7:AA:10:25:E8:23:FA:00:5F:BC:32:48:1E:F9:CB` |
| Политика | https://pirogovlab.ru/sanamaailma/privacy/ (с рекламой, live) |
| Страница игры | https://pirogovlab.ru/sanamaailma-igra/ |
| Тексты / формы | `release/store/TEXTS_ru.md`, `release/store/PLAY_FORMS.md` |
| Разработчик | PirogovLab / Михаил Пирогов · https://pirogovlab.ru · mihail.pirogov@gmail.com |

Порядок: §1 RuStore и §2 Google Play (параллельно) → §3 Яндекс Игры → §4 ссылка на магазин в РСЯ → §5 бейджи на сайте и в GitHub.

## 1. RuStore — https://console.rustore.ru
1. Приложения → «Создать приложение» → тип **Игра**, имя **Sanamaailma**, пакет `ru.pirogovlab.sanamaailma`.
2. Загрузить `release/sanamaailma.apk` (или `.aab`).
3. Карточка: краткое описание RuStore и полное из TEXTS_ru.md; «Что нового»: «Первая версия.»; категории **Словесные игры** + **Головоломки**; **0+**; иконка `release/rustore_assets/icon_512.png`; скриншоты `release/rustore_assets/mobile_1…6_*.png` (+ планшет `rustore_assets/tablet/`); баннер `release/rustore_assets/banner_1920x1080.png`; политика, сайт, email — как выше; реклама: **Да**, платный контент: нет.
4. На модерацию. После публикации — ссылку на карточку в §4.

## 2. Google Play — https://play.google.com/console/u/0/developers/8084969663799476138/app-list
**Сразу в Production (без закрытого теста)** — как «Марий мут» (ru.pirogovlab.mariwordle) в этом же аккаунте: он уже открыт в Google Play (https://play.google.com/store/apps/details?id=ru.pirogovlab.mariwordle отвечает 200, 19.10.2026). Значит, к аккаунту не применяется требование «12 тестировщиков × 14 дней» для новых личных аккаунтов (или оно уже выполнено). Проверка: в новом приложении «Панель управления»/«Опубликовать» должна быть доступна **«Рабочая версия» (Production)** без пункта «Подать заявку на доступ к рабочей версии». Если такой пункт появится — Production недоступен, нужен закрытый тест.
1. «Создать приложение»: **Sanamaailma**, язык по умолчанию **Русский (ru-RU)**, **Игра**, **Бесплатное**; отметить декларации.
2. «Содержание приложения» — все анкеты по `release/store/PLAY_FORMS.md` (политика, реклама, доступ, рекламный ID, аудитория 13+, Data safety, IARC, прочие декларации).
3. «Основная страница магазина»: краткое/полное описание (TEXTS_ru.md §1), значок `release/play_assets/play_icon_512.png`, графика `release/play_assets/feature_graphic_1024x500.png`, телефон `release/play_assets/screenshots/phone_1…7_*.png`, планшеты 7" и 10" `release/play_assets/tablet/tablet_1…7_*.png`. Необязательно: перевод страницы en-US из TEXTS_ru.md §3.
4. «Настройки магазина»: Игра → **Word**, теги, email, сайт https://pirogovlab.ru.
5. «Рабочая версия» → «Страны/регионы» (все) → «Создать выпуск» → принять **Play App Signing** (ключ Google; наш — ключ загрузки) → загрузить `release/sanamaailma.aab` → название выпуска `1.0.0 (1)`, примечания «Первая версия.» → «Проверить выпуск» → «Отправить на проверку» (обзор публикации). Первая проверка нового приложения — обычно до нескольких дней.

## 3. Яндекс Игры — https://games.yandex.ru/console
Всё по `release/YANDEX_CHECKLIST.md`: архив `release/sanamaailma-yandex.zip`, 1.0.0, язык ru, облачные сохранения ON, sticky-баннер через API ON, лидерборд `levels`; иконка `yandex_assets/icon_512x512.png`, обложка `cover_800x470.png`, витрина `cover_showcase_1560x520.png`, скриншоты `screenshot_mobile_*`, `screenshot_desktop_*`; тексты TEXTS_ru.md §2; политика — выше. Видео нет (необязательно). Проверить черновик с `?debug-mode=16`.

## 4. Рекламная сеть Яндекса — https://partner.yandex.ru/v2/inapp/app/20244945/edit/
После публикации в RuStore / Google Play добавить ссылку на магазин (пакет там не хранится) → модерация до ~2 дней → статус «Активно». app-ads.txt (`yandex.com, 1969132, DIRECT`) общий для аккаунта и уже на сайте; сайт разработчика в карточках магазинов — https://pirogovlab.ru. Код менять не нужно.

## 5. После публикации
- Сайт: на /sanamaailma-igra/ и /en/sanamaailma-igra/ у кнопок магазинов есть заготовки (`<!-- PLACEHOLDER stores -->`, атрибут `hidden`) — вписать href и убрать hidden.
- GitHub README: заменить комментарий `PLACEHOLDER store badges` ссылками.
- Решить, открывать ли веб-версию /sanamaailma/ для индексации (сейчас noindex + плашка «тестовая версия»; у других игр веб-версия открыта).
