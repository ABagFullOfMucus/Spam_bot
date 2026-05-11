from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import time

load_dotenv()

EMAIL = os.getenv("DISCORD_EMAIL")
PASSWORD = os.getenv("DISCORD_PASSWORD")
DM_URL = os.getenv("DM_URL")
MESSAGE = os.getenv("MESSAGE")

with sync_playwright() as p:
    browser = p.chromium.launch(headless = True)
    
    page  = browser.new_page()
    
    # login
    print("Navigating to Discord login page...")
    page.goto("https://discord.com/login")
    page.fill('input[name="email"]', EMAIL)
    page.fill('input[name="password"]', PASSWORD)
    
    page.keyboard.press("Enter")

    print("Waiting for navigation away from login page...")
    try:
        # Wait until the URL is no longer the login page (up to 30s)
        page.wait_for_url(lambda url: "discord.com/login" not in url, timeout=30000)
        print(f"Login appears successful — current URL: {page.url}")
    except Exception as e:
        print(f"Timed out waiting to leave login page: {e}")
        print(f"Current URL: {page.url}")
        print(f"Current page title: {page.title()}")
        print("Still on login page — login likely failed. Dumping page content...")
        print(page.content())
        page.screenshot(path="login_failed_screenshot.png")
        print("Screenshot saved to login_failed_screenshot.png")
        browser.close()
        raise SystemExit(1)

    # Confirm we are not still on the login page
    if "discord.com/login" in page.url:
        print(f"ERROR: Still on login page after wait. URL: {page.url}")
        print(f"Page title: {page.title()}")
        print("Dumping page content for debugging...")
        print(page.content())
        page.screenshot(path="login_failed_screenshot.png")
        print("Screenshot saved to login_failed_screenshot.png")
        browser.close()
        raise SystemExit(1)

    print(f"Login confirmed. Page title: {page.title()} | URL: {page.url}")

    # open DM
    print(f"Navigating to DM URL: {DM_URL}")
    page.goto(DM_URL)
    
    time.sleep(20)
    
    # send message
    print("Attempting to locate message input (textarea)...")
    try:
        textbox = page.locator('textarea')
        textbox.fill(MESSAGE)
        page.keyboard.press("Enter")
        print("Message sent!")
    except Exception as e:
        print(f"Failed to find or interact with textarea: {e}")
        print("Dumping page content for debugging...")
        print(page.content())
        page.screenshot(path="debug_screenshot.png")
        print("Screenshot saved to debug_screenshot.png")
    
    browser.close()