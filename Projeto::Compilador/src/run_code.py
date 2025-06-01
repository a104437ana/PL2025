import asyncio
import sys
from pyppeteer import launch
from pyppeteer import errors

async def runCode(code: str, url: str=None):
    browser = await launch(
        headless=False,
        executablePath=r"C:\Program Files\Google\Chrome\Application\chrome.exe" # Chrome path
    )
    page = await browser.newPage()

    close = asyncio.Event()
    page.on('close', close.set)

    try:
        await page.goto(url or 'http://localhost:27018')
    except errors.PageError as e:
        await browser.close()
        print("Cannot connect to page")
        sys.exit()

    await page.waitForSelector('#monaco-editor-container') # Input
    await page.click('#monaco-editor-container')

    await page.keyboard.type(code)

    await page.waitForSelector('#run_btn') # Run
    await page.click('#run_btn')

    await close.wait()

    await browser.close()

