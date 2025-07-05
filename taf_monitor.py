import asyncio
from playwright.async_api import async_playwright
import json
import os

URL = "http://zd.taf.org.cn/#/"
DATA_FILE = "taf_5g_products.json"

async def fetch_products(page):
    await page.goto(URL)
    # Wait for the table to load (adjust selector if needed)
    await page.wait_for_timeout(5000)  # Wait 5 seconds for JS to load

    # Try to get all table rows (adjust selector if needed)
    rows = await page.query_selector_all('table tbody tr')
    products = []
    for row in rows:
        cells = await row.query_selector_all('td')
        product = [await cell.inner_text() for cell in cells]
        products.append(product)
    return products

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        products = await fetch_products(page)
        await browser.close()

        # Load previous data if exists
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                old_products = json.load(f)
        else:
            old_products = []

        # Compare and notify
        if products != old_products:
            print("New products detected or product list updated!")
            # Save new data
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(products, f, ensure_ascii=False, indent=2)
        else:
            print("No new products.")

if __name__ == "__main__":
    asyncio.run(main())
