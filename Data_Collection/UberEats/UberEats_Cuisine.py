#Import necessary libraies
import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

# Set up ChromeDriver as per path and change if necessary
chrome_driver_path = r"C:\WebDriver\chromedriver.exe"  
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-popup-blocking")  
driver = webdriver.Chrome(service=service, options=options)

# iNPUT and output file 
input_csv = "UberEats_URL_Davis.csv"
output_csv = "UberEats_Cuisine.csv"

with open(input_csv, newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  
    restaurants = [row for row in reader]  # Reads all restaurants
cuisine_data = []

for name, url in restaurants:
    driver.get(url)
    time.sleep(5)  

    # Closes any cookie pop-up
    try:
        cookie_button = driver.find_element(By.XPATH, '//*[@id="cookie-banner-dismiss"]')
        cookie_button.click()
        time.sleep(2)
    except NoSuchElementException:
        pass 

    # Click on button to get restaurant details
    try:
        info_button = driver.find_element(By.XPATH, '//a[contains(@href, "mod=storeInfo")]')
        driver.execute_script("arguments[0].click();", info_button)
        time.sleep(5)  # Wait for info page to avoiding getting blocked
    except NoSuchElementException:
        print(f"❌ Info button not found for {name}")
        continue  # Skip 

    # Extract Cuisine and clean ing
    try:
        cuisine_element = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[4]/div/div/div[2]/div[3]/div[2]/div[2]/div[2]')
        raw_cuisine = cuisine_element.text
        # Extract only words and remove special characters like ,
        cuisine_list = re.findall(r'[A-Za-z&]+', raw_cuisine)  
        cuisine = ", ".join(cuisine_list)
    except NoSuchElementException:
        cuisine = "N/A"

    print(f"{name} - {cuisine}")
    cuisine_data.append([name, cuisine])

# Save to CSV file 
with open(output_csv, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Cuisine"])
    writer.writerows(cuisine_data)

print(f"\n✅ Extracted cuisine for {len(cuisine_data)} restaurants and saved to {output_csv}")
driver.quit()
