// scraper.js
const { chromium } = require('playwright'); // version Node.js

const URL = "https://m.leboncoin.fr/recherche?category=9&real_estate_type=1&regions=13&square_min=3000";

(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    await page.goto(URL, { timeout: 60000 });
    await page.waitForSelector("a[data-qa-id='aditem_container']", { timeout: 60000 });

    const ads = await page.$$("a[data-qa-id='aditem_container']");
    const results = [];

    for (const ad of ads) {
        const title = await ad.$eval("p[data-qa-id='aditem_title']", el => el.innerText).catch(() => null);
        const price = await ad.$eval("span[data-qa-id='aditem_price']", el => el.innerText).catch(() => null);
        const location = await ad.$eval("p[data-qa-id='aditem_location']", el => el.innerText).catch(() => null);

        let url = await ad.getAttribute("href");
        if (url && !url.startsWith("http")) {
            url = "https://m.leboncoin.fr" + url;
        }

        // Surface
        let surface = null;
        const tags = await ad.$$eval("div[data-qa-id='aditem_tags'] span", els => els.map(e => e.innerText));

        for (const t of tags) {
            if (t.includes("m²")) {
                const num = parseInt(t.replace("m²", "").trim());
                if (!isNaN(num)) surface = num;
            }
        }

        if (surface && surface >= 3000) {
            results.push({
                titre: title,
                prix: price,
                surface,
                ville: location,
                url,
                source: "leboncoin"
            });
        }
    }

    console.log(JSON.stringify(results));
    await browser.close();
})();
