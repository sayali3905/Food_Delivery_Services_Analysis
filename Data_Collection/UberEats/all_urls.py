from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

#fetch URLs of all restuarants
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

restaurants = []  
seen_urls = set()  

try:
    driver.get("https://www.ubereats.com/feed?diningMode=DELIVERY&effect=&marketing_vistor_id=60d6ba84-15f2-4328-8649-50740d1c5a02&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMk1lbW9yaWFsJTIwVW5pb24lMjAtJTIwVW5pdmVyc2l0eSUyMG9mJTIwQ2FsaWZvcm5pYSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMmhlcmUlM0FwZHMlM0FwbGFjZSUzQTg0MDhseHg1LTNjNWM1NTNhMGI5YjBhYzcwZjE3YjI5OTBjY2M5MjgxJTIyJTJDJTIycmVmZXJlbmNlVHlwZSUyMiUzQSUyMmhlcmVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EzOC41NDA3NiUyQyUyMmxvbmdpdHVkZSUyMiUzQS0xMjEuNzQ4MDclN0Q%3D&ps=1&sf=JTVCJTdCJTIydXVpZCUyMiUzQSUyMjJjN2NmN2VmLTczMGYtNDMxZi05MDcyLTQ2YmMzOWY3YzAyMSUyMiUyQyUyMm9wdGlvbnMlMjIlM0ElNUIlN0IlMjJ1dWlkJTIyJTNBJTIyMmM3Y2Y3ZWYtNzMwZi00MzFmLTkwNzItMjZiYzM5ZjdjMDMyJTIyJTdEJTJDJTdCJTIydXVpZCUyMiUzQSUyMjJjN2NmN2VmLTczMGYtNDMxZi05MDcyLTI2YmMzOWY3YzAzMyUyMiU3RCUyQyU3QiUyMnV1aWQlMjIlM0ElMjIyYzdjZjdlZi03MzBmLTQzMWYtOTA3Mi0yNmJjMzlmN2MwMzQlMjIlN0QlMkMlN0IlMjJ1dWlkJTIyJTNBJTIyMmM3Y2Y3ZWYtNzMwZi00MzFmLTkwNzItMjZiYzM5ZjdjMDM1JTIyJTdEJTVEJTdEJTVE")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-testid='store-card']")))

    while True:
        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show more')]"))
            )
            print("Clicking 'Show more'...")
            show_more_button.click()
            
            WebDriverWait(driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except Exception as e:
            print("No more 'Show more' button or error clicking it:", e)
            break

    restaurant_elements = driver.find_elements(By.XPATH, "//a[@data-testid='store-card']")
    for restaurant_element in restaurant_elements:
        name = restaurant_element.find_element(By.TAG_NAME, "h3").text
        link = restaurant_element.get_attribute("href")
        if link not in seen_urls:  # Check if URL is already seen
            seen_urls.add(link)
            restaurants.append((name, link))
            print(f"Collected: {name}, URL: {link}")

finally:
    driver.quit()

with open('restaurants.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Restaurant Name", "URL"])  
    writer.writerows(restaurants)  

print(f"Total restaurants collected: {len(restaurants)}")
