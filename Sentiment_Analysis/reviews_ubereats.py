import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re  

options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--headless")  
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def is_standalone_number_or_time(text):
    text = text.strip()
    if re.fullmatch(r"\d+(\.\d+)?\+?", text):  
        return True
    time_patterns = [
        r"^\d{1,2}:\d{2} (AM|PM|am|pm)$",  
        r"^\d{1,2} ?(AM|PM|am|pm)$", 
        r"^\d{1,2}:\d{2} (AM|PM|am|pm) - \d{1,2}:\d{2} (AM|PM|am|pm)$", 
    ]
    for pattern in time_patterns:
        if re.fullmatch(pattern, text):
            return True
    return False

def scrape_ubereats_reviews(url, max_scrolls=10):
    driver.get(url)
    time.sleep(5)  
    for _ in range(max_scrolls):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(3)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "p")))
    except Exception:
        return []

    soup = BeautifulSoup(driver.page_source, "html.parser")
    review_elements = soup.find_all("p", {"data-baseweb": "typo-paragraphsmall"})
    
    reviews = [
        review.get_text(strip=True)
        for review in review_elements
        if not is_standalone_number_or_time(review.get_text(strip=True))  
        and not any(keyword in review.get_text().lower() for keyword in [
            "this website uses third party advertising cookies",
            "reviews", "ratings"
        ])
    ]
    return reviews

def clean_text(text):
    if isinstance(text, float):  
        return ""
    time_pattern = r"(\d{1,2}:\d{2} [APap][Mm]\s*-\s*\d{1,2}:\d{2} [APap][Mm].*)"
    menu_pattern = r"(breakfast|lunch|dinner|menu|brunch|happy hour|all day)"
    if re.search(time_pattern, text) or re.search(menu_pattern, text.lower()):
        return ""
    return text

def process_urls_from_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    if "URL" not in df.columns:
        print("CSV file does not have column named URL.")
        return

    all_reviews = []

    for url in df["URL"].dropna():
        reviews = scrape_ubereats_reviews(url)
        for review in reviews:
            cleaned_review = clean_text(review)
            if cleaned_review:
                all_reviews.append({"URL": url, "Review": cleaned_review})

    output_df = pd.DataFrame(all_reviews)
    output_df.drop_duplicates(subset='Review', inplace=True)
    output_df.to_csv(output_csv, index=False)

input_csv = "restaurants_urls.csv" 
output_csv = "reviews_ubereats.csv"
process_urls_from_csv(input_csv, output_csv)

driver.quit()
