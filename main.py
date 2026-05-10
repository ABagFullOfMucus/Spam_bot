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
    page.goto("https://discord.com/login")
    page.fill('input[name="email"]', EMAIL)
    page.fill('input[name="password"]', PASSWORD)
    
    page.keyboard.press("Enter")
    
    time.sleep(10)
    
    # open DM
    page.goto(DM_URL)
    
    time.sleep(5)
    
    # send message
    
    textbox = page.locator('div[role="textbox"]')
    
    textbox.fill(MESSAGE)
    
    page.keyboard.press("Enter")
    
    print("message sent!")
    
    browser.close()