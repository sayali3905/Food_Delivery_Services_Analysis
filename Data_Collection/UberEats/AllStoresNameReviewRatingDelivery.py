#Import necessary libaries 
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

# Set up ChromeDriver according to path and update if required
chrome_driver_path = r"C:\WebDriver\chromedriver.exe"  
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# URL for Uber Eats delivery in Davis
url = "https://www.ubereats.com/feed?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMk1lbW9yaWFsJTIwVW5pb24lMjAtJTIwVW5pdmVyc2l0eSUyMG9mJTIwQ2FsaWZvcm5pYSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMmhlcmUlM0FwZHMlM0FwbGFjZSUzQTg0MDhseHg1LTNjNWM1NTNhMGI5YjBhYzcwZjE3YjI5OTBjY2M5MjgxJTIyJTJDJTIycmVmZXJlbmNlVHlwZSUyMiUzQSUyMmhlcmVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EzOC41NDA3NiUyQyUyMmxvbmdpdHVkZSUyMiUzQS0xMjEuNzQ4MDclN0Q%3D&ps=1&sf=JTVCJTdCJTIydXVpZCUyMiUzQSUyMjJjN2NmN2VmLTczMGYtNDMxZi05MDcyLTQ2YmMzOWY3YzAyMSUyMiUyQyUyMm9wdGlvbnMlMjIlM0ElNUIlN0IlMjJ1dWlkJTIyJTNBJTIyMmM3Y2Y3ZWYtNzMwZi00MzFmLTkwNzItMjZiYzM5ZjdjMDMyJTIyJTdEJTJDJTdCJTIydXVpZCUyMiUzQSUyMjJjN2NmN2VmLTczMGYtNDMxZi05MDcyLTI2YmMzOWY3YzAzMyUyMiU3RCUyQyU3QiUyMnV1aWQlMjIlM0ElMjIyYzdjZjdlZi03MzBmLTQzMWYtOTA3Mi0yNmJjMzlmN2MwMzQlMjIlN0QlMkMlN0IlMjJ1dWlkJTIyJTNBJTIyMmM3Y2Y3ZWYtNzMwZi00MzFmLTkwNzItMjZiYzM5ZjdjMDM1JTIyJTdEJTVEJTdEJTVE"
driver.get(url)
time.sleep(10)  # Wait for initial lOAd
time.sleep(30)  # wait time for manual scrolling 

# Manual scrolling
restaurants = driver.find_elements(By.XPATH, '//*[@id="main-content"]/div/div[4]/div/div/div[4]/div')
restaurant_data = []

for i, restaurant in enumerate(restaurants, start=1):  # Extract all restaurants
    try:
        name = restaurant.find_element(By.XPATH, './/div/div/div/div/div[2]/div[1]/div[1]').text
        rating = restaurant.find_element(By.XPATH, './/div/div/div/div/div[2]/div[3]/span[1]').text
        reviews = restaurant.find_element(By.XPATH, './/div/div/div/div/div[2]/div[3]/span[2]').text.strip()
        delivery_time = restaurant.find_element(By.XPATH, './/div/div/div/div/div[2]/div[3]/span[4]').text
        reviews = reviews.replace("(", "").replace(")", "").replace("-", "")  # Remove unwanted characters
        
        restaurant_data.append([name, rating, reviews, delivery_time])
        print(f"{i}. {name} - {rating} ({reviews}) - {delivery_time}")
    except:
        pass  # Skip missing Data

# Save to CSV file to AllStoresNameReviewRatingDelivery.csv
csv_file = "AllStoresNameReviewRatingDelivery.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Rating", "Reviews", "Delivery Time"])  
    writer.writerows(restaurant_data)  

print(f"\n✅ Extracted {len(restaurant_data)} restaurants and saved to {csv_file}")
driver.quit()

