import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

input_csv = "restaurants_urls.csv"  
output_csv = "reviews_grubhub.csv"
df = pd.read_csv(input_csv)

if 'URL' not in df.columns:
    raise ValueError("CSV file must contain a column named 'url'")

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

reviews_data = []
for index, row in df.iterrows():
    url = row['URL']
    
    try:
        driver.get(url)
        time.sleep(5)  
        soup = BeautifulSoup(driver.page_source, "html.parser")
        reviews = soup.find_all("span", {"data-testid": "review-content"})
        if reviews:
            for review in reviews:
                reviews_data.append([url, review.text.strip()])
        else:
            reviews_data.append([url, "No reviews found"])
    except Exception as e:
        print(f"Error fetching reviews for {url}: {e}")
        reviews_data.append([url, f"Error: {e}"])
driver.quit()

reviews_df = pd.DataFrame(reviews_data, columns=["URL", "Review"])
reviews_df.to_csv(output_csv, index=False, encoding="utf-8")
print(f"\nReviews saved to {output_csv}")
