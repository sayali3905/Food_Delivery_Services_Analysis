import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager

#Fetching menu of all restuarants
options = webdriver.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-webgl")  
options.add_argument("--enable-unsafe-swiftshader")  

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def extract_menu_items(url):
    driver.get(url)
    time.sleep(5)  
    soup = BeautifulSoup(driver.page_source, "html.parser")
    items = soup.find_all("span", {"data-testid": "rich-text"})
    menu = []
    for i in range(len(items) - 1):
        name = items[i].text.strip()
        if name.startswith("$"):  
            continue
        if i + 1 < len(items) and items[i + 1].text.strip().startswith("$"):
            price = items[i + 1].text.strip()
            menu.append((name, price))
    return menu


output_csv = "combined_menus.csv"
with open(output_csv, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Restaurant Name', 'Item Name', 'Price'])  

    
    csv_file = "restaurants.csv"
    try:
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            restaurant_data = [row for row in reader]
    except UnicodeDecodeError:
        with open(csv_file, newline='', encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file)
            restaurant_data = [row for row in reader]

    for row in restaurant_data:
        restaurant_name = row['Restaurant Name']
        url = row['URL']
        print(f"Extracting menu for {restaurant_name}")
        menu = extract_menu_items(url)
        # Write to the same CSV
        for item in menu:
            writer.writerow([restaurant_name] + list(item))
        writer.writerow([])  


driver.quit()
