from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import re

# ============ CONFIG ============
BASE_URL = "https://www.shl.com"
CATALOG_URL = BASE_URL + "/products/product-catalog/"
OUTPUT_FILE = "./final_data.csv"

# ============ SETUP DRIVER ============
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get(CATALOG_URL)
time.sleep(3)

data = []

# ============ SCRAPE LISTING PAGE ============
def extract_page_data(soup):
    rows = soup.select("div.custom__table-responsive tr[data-entity-id], tr[data-course-id]")
    
    for row in rows:
        title_cell = row.select_one("td.custom__table-heading__title a")
        remote = row.select_one("td:nth-of-type(2) span.catalogue__circle.-yes")
        adaptive = row.select_one("td:nth-of-type(3) span.catalogue__circle.-yes")
        test_type_cell = row.select_one("td:nth-of-type(4) span.product-catalogue__key")

        name = title_cell.text.strip() if title_cell else "N/A"
        link = BASE_URL + title_cell['href'] if title_cell else "N/A"
        remote_testing = "Yes" if remote else "No"
        adaptive_support = "Yes" if adaptive else "No"
        test_type = test_type_cell.text.strip() if test_type_cell else "N/A"

        data.append({
            "Test Name": name,
            "Test Link": link,
            "Remote Testing": remote_testing,
            "Adaptive/IRT": adaptive_support,
            "Test Type": test_type
        })

# ============ PAGINATION ============
while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    extract_page_data(soup)

    try:
        next_button = driver.find_element(By.XPATH, '//a[contains(text(),"Next")]')
        if "disabled" in next_button.get_attribute("class"):
            break
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(2)
    except:
        break

driver.quit()

# ============ SCRAPE DURATION FROM EACH PAGE ============
def get_duration(url):
    try:
        res = requests.get(url, timeout=5)
        if res.status_code != 200:
            return "N/A"
        soup = BeautifulSoup(res.text, "html.parser")

        # Extract using updated pattern
        match = re.search(r"Approximate Completion Time in minutes\s*=\s*(\d+)", soup.get_text(), re.IGNORECASE)
        if match:
            return f"{match.group(1)} minutes"
    except Exception as e:
        print(f"Error scraping duration from {url}: {e}")
    return "N/A"

# ============ ADD DURATION TO EACH ENTRY ============
for i, entry in enumerate(data):
    print(f"[{i+1}/{len(data)}] Scraping duration from: {entry['Test Link']}")
    entry["Duration"] = get_duration(entry["Test Link"])
    time.sleep(1)

# ============ SAVE TO CSV ============
df = pd.DataFrame(data)
df.to_csv(OUTPUT_FILE, index=False)
print(f"\nAll done! Data saved to {OUTPUT_FILE}")