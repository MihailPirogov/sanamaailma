// Promo art for Sanamaailma -> release/art_src/{feature,cover,banner,og}_raw.png. Usage: node release/art_src/render.js
const { chromium } = require(require('path').join(__dirname, '../test/node_modules/playwright-core'));
const path = require('path');
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox', '--allow-file-access-from-files'] });
  for (const k of ['feature', 'cover', 'banner', 'og', 'showcase']) {
    const p = await b.newPage({ viewport: { width: 2000, height: 1100 } });
    await p.goto('file://' + path.join(__dirname, 'art.html'));
    const [w, h] = await p.evaluate(k => render(k), k);
    await p.setViewportSize({ width: w, height: h }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(900);
    await p.locator('#c').screenshot({ path: path.join(__dirname, k + '_raw.png') });
    await p.close();
  }
  await b.close();
})();
