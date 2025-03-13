import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")  
options.add_argument("--no-sandbox")  
options.add_argument("--disable-software-rasterizer")  
options.add_argument("--enable-unsafe-swiftshader") 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = 'https://www.grubhub.com/lets-eat'
driver.get(url)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.restaurant-name")))
last_height = driver.execute_script("return document.body.scrollHeight")
new_height = last_height
while new_height >= last_height:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3) 
    last_height = new_height
    new_height = driver.execute_script("return document.body.scrollHeight")

try:
    restaurant_links = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.restaurant-name"))
    )
    data = []
    base_url = 'https://www.grubhub.com'
    for link in restaurant_links:
        relative_url = link.get_attribute('href')
        if relative_url:
            if relative_url.startswith('/'):
                full_url = base_url + relative_url
            else:
                full_url = relative_url
            restaurant_name = link.get_attribute('title')
            data.append([restaurant_name, full_url])

    with open('restaurants_urls.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Restaurant Name', 'URL'])  
        writer.writerows(data) 
except Exception as e:
    print(f"Error while extracting links: {e}")

driver.quit()
