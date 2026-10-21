/* Yandex Advertising Network (RSYa) WEB block IDs for the public site build only (https://pirogovlab.ru/sanamaailma/).
 * Loaded by tools/stage_public.sh together with js/adapters/web.js. NOT used by the Yandex Games build (Games SDK)
 * nor by the Android build (Yandex Mobile Ads, android/app/src/main/res/values/ads.xml).
 * Empty string = off (RSYa site moderation pending until 20.11.2026). Put the real R-A-<site>-<n> units here later. While an ID is empty/invalid,
 * that ad type is simply off (no request to yandex.ru is made for it). */
window.WEBADS_CONFIG = {
  banner: '',        // sticky banner at the bottom of the screen (renderTo)
  interstitial: '',  // type: 'fullscreen' — between levels, every 3rd win, >= 150 s apart
  rewarded: '',      // SEPARATE fullscreen block used for rewards (RSYa web has no rewarded format):
                                  // hint / ×2 coins / extra spin (up to 3 a day) are granted only if this fullscreen ad was shown and closed
  loader: 'https://yandex.ru/ads/system/context.js',
};
