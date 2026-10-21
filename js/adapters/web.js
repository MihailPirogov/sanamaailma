/* Public web adapter (pirogovlab.ru/sanamaailma/): Yandex Advertising Network web (RTB) units via the Yandex.RTB loader.
 * Included ONLY by tools/stage_public.sh (never by tools/build_release.py yandex/android).
 * Block IDs: js/webads_config.js. The show points and caps stay in js/app.js (same for all platforms):
 *   banner after the tutorial; fullscreen every 3rd win and >= 150 s apart; rewarded only on the player's tap.
 * RSYa web has no 'rewarded' format: rewards use a SEPARATE fullscreen block (WEBADS_CONFIG.rewarded) and are granted
 * only when that ad actually rendered and was closed; error / no fill / nothing shown -> no reward (game shows 'ad failed' as on other platforms).
 * Graceful: blocked loader / no fill / placeholder IDs -> that ad type reports unavailable (🎬 buttons hidden), no errors. */
(function () {
  if (window.__adsim) return;                      // ?adsim=1 test simulation wins
  const C = window.WEBADS_CONFIG || {};
  const real = id => typeof id === 'string' && /^R-A-\d+-\d+$/.test(id);
  const want = { banner: real(C.banner), interstitial: real(C.interstitial), rewarded: real(C.rewarded) };
  const log = window.__webads = [];
  if (!want.banner && !want.interstitial && !want.rewarded) { Platform.use({ name: 'web' }); return; }
  let ready = false, failed = false;
  const cool = { interstitial: 0, rewarded: 0 };   // after a no-fill, don't offer that type for a minute
  const ping = () => { try { window.dispatchEvent(new Event('platform:ads')); } catch (e) {} };
  window.yaContextCb = window.yaContextCb || [];
  const s = document.createElement('script'); s.async = true; s.src = C.loader || 'https://yandex.ru/ads/system/context.js';
  s.onload = () => { window.yaContextCb.push(() => { ready = !!(window.Ya && Ya.Context && Ya.Context.AdvManager); log.push('ready ' + ready); ping(); }); };
  s.onerror = () => { failed = true; log.push('loader blocked'); hideBanner(); ping(); };
  document.head.appendChild(s);
  const AM = () => (window.Ya && Ya.Context && Ya.Context.AdvManager) || null;
  const plat = () => (matchMedia('(pointer:coarse)').matches ? 'touch' : 'desktop');
  const ok = k => want[k] && !failed && ready && !!AM() && Date.now() >= cool[k];
  function render(opts) { window.yaContextCb.push(() => { try { AM().render(opts); } catch (e) { opts.onError && opts.onError(e); } }); }
  // fullscreen / rewarded: resolve on close; on error or if nothing renders within 8 s -> fail softly
  function full(kind, blockId) {
    return new Promise(res => {
      let done = false, shown = false;
      const fin = (v, why) => { if (done) return; done = true; clearTimeout(t); Platform.audio.resume('ad'); log.push(kind + ' ' + why); res(v); };
      const t = setTimeout(() => { if (!shown) { cool[kind] = Date.now() + 60000; fin(false, 'timeout'); ping(); } }, 8000);
      Platform.audio.suspend('ad');
      const o = { blockId, type: 'fullscreen', platform: plat(),
        onRender: () => { shown = true; log.push(kind + ' render'); },
        onClose: () => fin(shown, 'close'),          // reward = the fullscreen ad was really shown
        onError: e => { cool[kind] = Date.now() + 60000; fin(false, 'error'); ping(); } };
      render(o);
    });
  }
  let bannerEl = null;
  function hideBanner() { if (bannerEl) { bannerEl.remove(); bannerEl = null; } document.documentElement.classList.remove('withBanner'); }
  Platform.use({
    name: 'web',
    ads: {
      rewardedAvailable() { return ok('rewarded'); },
      showRewarded() { return ok('rewarded') ? full('rewarded', C.rewarded) : Promise.resolve(false); },
      interstitialAvailable() { return ok('interstitial'); },
      async showInterstitial() { if (ok('interstitial')) await full('interstitial', C.interstitial); },
      bannerAvailable() { return want.banner && !failed; },
      showBanner() {
        if (!want.banner || failed || bannerEl) return;
        bannerEl = document.createElement('div'); bannerEl.id = 'webAdBanner'; document.body.appendChild(bannerEl);
        document.documentElement.classList.add('withBanner'); log.push('banner+');
        render({ blockId: C.banner, renderTo: 'webAdBanner', onRender: () => log.push('banner render'), onError: () => { log.push('banner error'); hideBanner(); } });
      },
      hideBanner() { if (bannerEl) log.push('banner-'); hideBanner(); },
    },
  });
})();
