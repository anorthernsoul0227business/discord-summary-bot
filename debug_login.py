import asyncio
from playwright.async_api import async_playwright
from config import Config

async def debug():
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=True)
    page = await browser.new_page()
    await page.goto("https://discord.com/login")
    await page.wait_for_load_state("networkidle")
    await page.locator('input[name="email"]').fill(Config.DISCORD_EMAIL)
    await page.locator('input[name="password"]').fill(Config.DISCORD_PASSWORD)
    await page.locator('button[type="submit"]').click()
    await page.wait_for_timeout(10000)
    await page.screenshot(path="/root/debug_login.png")
    print("スクリーンショット保存完了: /root/debug_login.png")
    await browser.close()

asyncio.run(debug())
