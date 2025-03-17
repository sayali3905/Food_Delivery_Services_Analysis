#Import necessary libraies
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Path to Chrome WebDriver, update as required
CHROME_DRIVER_PATH = r"C:\WebDriver\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-notifications")

service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Load restaurant URLs and names from given csv which contains URLs
df = pd.read_csv("UberEats_URL_Davis.csv")
restaurant_data = df[["Name", "URL"]].values[:] 
scraped_data = []

for name, url in restaurant_data:
    driver.get(url)
    time.sleep(3)
#remove any pop up for cookies tab
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accept') or contains(text(),'OK')]"))
        )
        cookie_button.click()
    except:
        pass
#find element for address 
    try:
        address_element = driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div[1]/div/div[3]/div/div/div[1]/div/p[2]/span')
        address = address_element.text.strip()
    except:
        address = "N/A"

    scraped_data.append({"Name": name, "URL": url, "Address": address})
    print(f"{name} - {address}")

# Save results to CSV address.csv
pd.DataFrame(scraped_data).to_csv("UberEats_Address.csv", index=False)
driver.quit()
