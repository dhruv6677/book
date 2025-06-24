from playwright.sync_api import sync_playwright
import os
from bs4 import BeautifulSoup
import sys


def scrape_chapter(url, screenshot_path="assets/screenshot.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"Navigating to {url}")
        page.goto(url)

        page.wait_for_selector("#mw-content-text .mw-parser-output")

        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        page.screenshot(path=screenshot_path, full_page=True)

        content = page.locator(
            "#mw-content-text .mw-parser-output").first.inner_text()

        browser.close()
        return content


if __name__ == "__main__":
    # Usage: python scraper.py <chapter_number>
    if len(sys.argv) < 2:
        print("❌ Please provide a chapter number.")
        sys.exit(1)

    chapter_num = sys.argv[1]
    base_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_{}"
    chapter_url = base_url.format(chapter_num)

    content = scrape_chapter(chapter_url)

    os.makedirs("assets", exist_ok=True)
    with open(f"assets/chapter{chapter_num}_raw.txt", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Chapter {chapter_num} scraped and saved.")
