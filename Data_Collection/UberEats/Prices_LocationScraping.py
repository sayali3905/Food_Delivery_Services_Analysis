#Import necessary libraied
import os
import csv
from bs4 import BeautifulSoup

# Path containing the HTML files
folder_path = r"C:\Users\ADMIN\OneDrive\Desktop\UC DAVIS\STA 220\UberEats_NewYork_Orders"
folder_name = os.path.basename(folder_path)

# Creates the CSV filename based on the folder name same 
output_csv = f"{folder_name}.csv"
with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)  # Ensure proper quoting
    writer.writerow(["Restaurant Name", "Item Name", "Quantity", "Price", "Subtotal", "Delivery Fee", "Taxes & Other Fees", "Total"])

    # Loop 
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            # Extract restaurant name
            all_labels = soup.select("div[data-baseweb='typo-labelmedium']")
            restaurant_name = all_labels[1].text.strip() if len(all_labels) > 1 else "Not Found"

            # Extract cart items
            cart_summary = soup.select_one("ul[data-baseweb='accordion'] li[data-testid='cart-summary-panel']")
            
            if cart_summary:
                cart_items = cart_summary.find_all("li")
                
                # Extract fare breakdown
                fare_breakdown = soup.select_one("div[data-test='fare-breakdown']")
                if fare_breakdown:
                    breakdown_items = fare_breakdown.find("ul").find_all("li")
                    subtotal = breakdown_items[0].find("span").text.strip() if len(breakdown_items) > 0 else "Not Found"
                    delivery_fee = breakdown_items[1].find("span").text.strip() if len(breakdown_items) > 1 else "Not Found"
                    taxes_fees = breakdown_items[2].find("span").text.strip() if len(breakdown_items) > 2 else "Not Found"
                    
                    total_div = fare_breakdown.find_all("div")[-1]
                    total_value = total_div.find_next_sibling(string=True).strip() if total_div else "Not Found"
                    if not total_value:
                        total_value = total_div.find("span").get_text(strip=True) if total_div.find("span") else "Not Found"
                else:
                    subtotal, delivery_fee, taxes_fees, total_value = "Not Found", "Not Found", "Not Found", "Not Found"

                # Extract and writing of all items to CSV
                for item in cart_items:
                    name_tag = item.select_one("a[class] div:nth-of-type(2) div:nth-of-type(1)")
                    item_name = name_tag.text.strip() if name_tag else "Not Found"

                    price_tag = item.select_one("a[class] div:nth-of-type(2) div:nth-of-type(3)")
                    item_price = price_tag.text.strip() if price_tag else "Not Found"

                    quantity_tag = item.select_one("div > div > div > ul > li > div > div")
                    item_quantity = quantity_tag.get_text(strip=True) if quantity_tag else "1"

                    writer.writerow([restaurant_name, item_name, item_quantity, item_price, subtotal, delivery_fee, taxes_fees, total_value])

            # Print 
            print(f"Processed: {filename}")
print(f"Data saved to {output_csv}")
