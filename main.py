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
    
    print("Waiting for page to reach network idle after login...")
    page.wait_for_load_state("domcontentloaded")
    
    time.sleep(10)
    
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