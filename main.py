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
    page.wait_for_load_state("networkidle")
    
    time.sleep(10)
    
    # open DM
    print(f"Navigating to DM URL: {DM_URL}")
    page.goto(DM_URL)
    
    time.sleep(10)
    
    # send message
    print("Waiting for textbox to appear...")
    page.wait_for_selector('div[role="textbox"]', timeout=15000)
    
    print("Textbox found, filling message...")
    textbox = page.locator('div[role="textbox"]')
    
    textbox.fill(MESSAGE)
    
    page.keyboard.press("Enter")
    
    print("Message sent!")
    
    browser.close()