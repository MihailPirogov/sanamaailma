// Sanamaailma app icon from Art.iconSvg (js/art.js) -> img/icon.png (512), img/icon.svg, release/art_src/icon_{1024,full_1024}.png
// and the legacy/round Android launcher PNGs (Android 7.x). Adaptive layers (foreground/background) are kept as they are.
// Usage: node tools/make_icons.js   (then python3 tools/make_icons_post.py)
const { chromium } = require(require('path').join(__dirname, '../test/node_modules/playwright-core'));
const path = require('path'), fs = require('fs'); const ROOT = path.resolve(__dirname, '..');
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox', '--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1024, height: 1024 } });
  fs.writeFileSync('/tmp/icon_page.html', `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://${ROOT}/css/fonts.css"><style>html,body{margin:0;background:transparent}svg{display:block;width:1024px;height:1024px}</style></head><body><div id="i"></div><script src="file://${ROOT}/js/art.js"></script></body></html>`);
  await p.goto('file:///tmp/icon_page.html'); await p.evaluate(() => document.fonts.load('800 150px Unbounded'));
  for (const [rx, out] of [[112, 'icon_1024.png'], [0, 'icon_full_1024.png']]) {
    await p.evaluate(rx => { document.getElementById('i').innerHTML = Art.iconSvg(rx); }, rx); await p.waitForTimeout(400);
    await p.locator('svg').screenshot({ path: path.join(ROOT, 'release/art_src', out), omitBackground: true });
  }
  fs.writeFileSync(path.join(ROOT, 'img/icon.svg'), await p.evaluate(() => Art.iconSvg(112)));
  await b.close();
})();
