import asyncio
from playwright.async_api import async_playwright

URL = "https://m.leboncoin.fr/recherche?category=9&real_estate_type=1&regions=13&square_min=3000"

async def scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(URL, timeout=60000)
        await page.wait_for_selector("a[data-qa-id='aditem_container']", timeout=60000)

        ads = await page.query_selector_all("a[data-qa-id='aditem_container']")
        results = []

        for ad in ads:
            title_el = await ad.query_selector("p[data-qa-id='aditem_title']")
            price_el = await ad.query_selector("span[data-qa-id='aditem_price']")
            loc_el = await ad.query_selector("p[data-qa-id='aditem_location']")

            title = await title_el.inner_text() if title_el else None
            price = await price_el.inner_text() if price_el else None
            location = await loc_el.inner_text() if loc_el else None

            url = await ad.get_attribute("href")
            if url and not url.startswith("http"):
                url = "https://m.leboncoin.fr" + url

            # Surface
            surface = None
            tags = await ad.query_selector_all("div[data-qa-id='aditem_tags'] span")
            for t in tags:
                txt = await t.inner_text()
                if "m²" in txt:
                    try:
                        surface = int(txt.replace("m²", "").strip())
                    except:
                        pass

            if surface and surface >= 3000:
                results.append({
                    "titre": title,
                    "prix": price,
                    "surface": surface,
                    "ville": location,
                    "url": url,
                    "source": "leboncoin"
                })

        return results

