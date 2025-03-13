import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

input_csv = "restaurants_urls.csv"  
output_csv = "menu.csv"  

with open(input_csv, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    restaurants = [(row['Restaurant Name'], row['URL']) for row in reader]

menu_data = []
for restaurant_name, url in restaurants:
    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//span[@data-testid="menu-item-price"]'))
        )
    except:
        print(f"Menu items did not load for {restaurant_name}.")
        continue

    for _ in range(10):  
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    
    items = soup.find_all("h6", class_="sc-kDvujY sc-ipEyDJ jJHOGL geYjwu u-text-ellipsis")
    prices = soup.find_all("span", {"data-testid": "menu-item-price"})  
    
    min_length = min(len(items), len(prices))
    
    for i in range(min_length):
        item_name = items[i].text.strip()
        item_price = prices[i].text.strip()
        menu_data.append([restaurant_name, item_name, item_price])
        print(f"{restaurant_name} - {item_name}: {item_price}")  

driver.quit()

with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Restaurant Name', 'Item Name', 'Price'])  
    writer.writerows(menu_data)
print(f"Menu data has been saved to '{output_csv}'")