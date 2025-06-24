import os
import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import sys

# --- CONFIGURATION ---
# Use URL from command line if provided, else default
URL = sys.argv[1] if len(sys.argv) > 1 else "https://books.toscrape.com/"
PRICE_ALERT_THRESHOLD = 20.0  # Set to None to disable alerts
PRICE_FILTER_MAX = None      # Only log books below this price (None = no filter)
TITLE_KEYWORD_FILTER = ''    # Only log books whose title contains this keyword (case-insensitive, '' = no filter)

CSV_PATH = os.path.join("data", "price_log.csv")

page_limit_arg = sys.argv[2] if len(sys.argv) > 2 else '1'
try:
    PAGE_LIMIT = int(page_limit_arg)
except ValueError:
    PAGE_LIMIT = 1

def scrape_all_books_paginated():
    """Scrape all book titles and prices from all pages (optionally in a category)."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = None
    books = []
    try:
        driver = webdriver.Chrome(options=options)
        next_url = URL
        pages_scraped = 0
        while next_url and pages_scraped < PAGE_LIMIT:
            driver.get(next_url)
            time.sleep(2)
            pages_scraped += 1
            products = driver.find_elements(By.CSS_SELECTOR, ".product_pod")
            for product in products:
                title = product.find_element(By.TAG_NAME, "h3").text.strip()
                price_text = product.find_element(By.CSS_SELECTOR, ".price_color").text.strip()
                price = float(price_text.replace('£', '').replace('$', '').strip())
                # Filtering
                if PRICE_FILTER_MAX is not None and price > PRICE_FILTER_MAX:
                    continue
                if TITLE_KEYWORD_FILTER and TITLE_KEYWORD_FILTER.lower() not in title.lower():
                    continue
                books.append({"title": title, "price": price})
                # Price alert
                if PRICE_ALERT_THRESHOLD is not None and price < PRICE_ALERT_THRESHOLD:
                    print(f"ALERT: '{title}' is now £{price:.2f}!")
            # Find next page
            try:
                next_btn = driver.find_element(By.CSS_SELECTOR, ".next > a")
                next_href = next_btn.get_attribute("href")
                next_url = next_href
            except Exception:
                next_url = None
        return books
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []
    finally:
        if driver:
            driver.quit()

def log_price(title, price):
    """Append the scraped data to the CSV file with a timestamp."""
    if not title or price is None:
        print("No data to log.")
        return
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    row = {"timestamp": timestamp, "title": title, "price": price}
    df = pd.DataFrame([row])

    # Ensure the file exists and ends with a newline
    if os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 0:
        with open(CSV_PATH, "rb+") as f:
            f.seek(-1, os.SEEK_END)
            last_char = f.read(1)
            if last_char != b"\n":
                f.write(b"\n")

    # Append to CSV, create if not exists, always use correct lineterminator
    header = not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0
    df.to_csv(CSV_PATH, mode='a', header=header, index=False, lineterminator='\n')
    print(f"Logged: {row}")

if __name__ == "__main__":
    books = scrape_all_books_paginated()
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    for book in books:
        log_price(book["title"], book["price"]) 