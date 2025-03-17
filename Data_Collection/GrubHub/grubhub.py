from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager

#To fetch menus
urls = [
    "https://www.grubhub.com/restaurant/panda-express-1491-w-covell-blvd-davis/1958456",
    "https://www.grubhub.com/restaurant/taco-bell-425-g-st-davis/1016840",
    "https://www.grubhub.com/restaurant/mcdonalds-4444-chiles-rd-davis/2457649",
    "https://www.grubhub.com/restaurant/jack-in-the-box-337-g-st-davis/2455132",
    "https://www.grubhub.com/restaurant/shake-shack-1710-r-st-sacramento/2216083",
    "https://www.grubhub.com/restaurant/mountain-mikes-pizza-1900-s-st-sacramento/3335401",
    "https://www.grubhub.com/restaurant/jacks-urban-eats-1321-w-covell-blvd-davis/2127430",
    "https://www.grubhub.com/restaurant/ikes-love--sandwiches-1420-16th-st-ste-100-sacramento/951426",
    "https://www.grubhub.com/restaurant/chipotle-227-e-st-davis/2125568",
    "https://www.grubhub.com/restaurant/ihop-1745-cowell-blvd-davis/2416051",
    "https://www.grubhub.com/restaurant/starbucks-2038-lyndell-terrace-davis/8308728"
]

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for url in urls:
    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//span[@data-testid="menu-item-price"]'))
        )
    except:
        print(f"Menu items did not load for {url}")
        continue

    for _ in range(10):
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    items = soup.find_all("h6", class_="sc-kDvujY sc-ipEyDJ jJHOGL geYjwu u-text-ellipsis")
    prices = soup.find_all("span", {"data-testid": "menu-item-price"})

    menu_data = []
    min_length = min(len(items), len(prices))
    for i in range(min_length):
        item_name = items[i].text.strip()
        item_price = prices[i].text.strip()
        menu_data.append([item_name, item_price])

    filename = f"{url.split('/')[-2]}.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Item Name', 'Price'])
        writer.writerows(menu_data)

    print(f"Menu data has been saved to '{filename}'")

driver.quit()
