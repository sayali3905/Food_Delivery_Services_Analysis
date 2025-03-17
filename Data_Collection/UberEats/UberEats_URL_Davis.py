#Import all necessary libraries
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Set up ChromeDriver and give path 
chrome_driver_path = r"C:\WebDriver\chromedriver.exe"  # Update accordingly
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# URL for Uber Eats restaurants of davis
url = "https://www.ubereats.com/feed?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMk1lbW9yaWFsJTIwVW5pb24lMjAtJTIwVW5pdmVyc2l0eSUyMG9mJTIwQ2FsaWZvcm5pYSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMmhlcmUlM0FwZHMlM0FwbGFjZSUzQTg0MDhseHg1LTNjNWM1NTNhMGI5YjBhYzcwZjE3YjI5OTBjY2M5MjgxJTIyJTJDJTIycmVmZXJlbmNlVHlwZSUyMiUzQSUyMmhlcmVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EzOC41NDA3NiUyQyUyMmxvbmdpdHVkZSUyMiUzQS0xMjEuNzQ4MDclN0Q%3D&ps=1&sf=JTVCJTdCJTIydXVpZCUyMiUzQSUyMjJjN2NmN2VmLTczMGYtNDMxZi05MDcyLTQ2YmMzOWY3YzAyMSUyMiUyQyUyMm9wdGlvbnMlMjIlM0ElNUIlN0IlMjJ1dWlkJTIyJTNBJTIyMmM3Y2Y3ZWYtNzMwZi00MzFmLTkwNzItMjZiYzM5ZjdjMDMyJTIyJTdEJTJDJTdCJTIydXVpZCUyMiUzQSUyMjJjN2NmN2VmLTczMGYtNDMxZi05MDcyLTI2YmMzOWY3YzAzMyUyMiU3RCUyQyU3QiUyMnV1aWQlMjIlM0ElMjIyYzdjZjdlZi03MzBmLTQzMWYtOTA3Mi0yNmJjMzlmN2MwMzQlMjIlN0QlMkMlN0IlMjJ1dWlkJTIyJTNBJTIyMmM3Y2Y3ZWYtNzMwZi00MzFmLTkwNzItMjZiYzM5ZjdjMDM1JTIyJTdEJTVEJTdEJTVE"
driver.get(url)
time.sleep(10)  # Wait for initial load to avoid getting blocked 

time.sleep(30)  # wait time for manual scrolling 

# Manual scrolling
restaurants = driver.find_elements(By.XPATH, '//*[@id="main-content"]/div/div[4]/div/div/div[4]/div')
restaurant_data = []
base_url = "https://www.ubereats.com"

for i, restaurant in enumerate(restaurants, start=1):  # Get all restaurants
    try:
        link_element = restaurant.find_element(By.XPATH, './/div/div/div/a')
        name = link_element.text
        url = link_element.get_attribute("href")
        
        if not url.startswith("http"):
            url = base_url + url
        
        restaurant_data.append([name, url])
        print(f"{i}. {name} - {url}")
    except:
        pass  # Skip misssing data 

# Save results to UberEats_URL_Davis.csv 
csv_file = "UberEats_URL_Davis.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "URL"]) 
    writer.writerows(restaurant_data)  

print(f"\n✅ Extracted {len(restaurant_data)} restaurants and saved to {csv_file}")
driver.quit()
