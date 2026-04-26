const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err.message));
  await page.goto('http://localhost:3000/impressum');
  const hasCanvas = await page.evaluate(() => {
    return document.querySelectorAll('.particles-js-canvas-el').length > 0;
  });
  console.log('HAS CANVAS:', hasCanvas);
  
  const zIndex = await page.evaluate(() => {
    const el = document.getElementById('particles-bg');
    return el ? window.getComputedStyle(el).zIndex : null;
  });
  console.log('Z-INDEX:', zIndex);
  
  await browser.close();
})();
