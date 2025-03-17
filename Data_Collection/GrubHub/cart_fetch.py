import csv
import os
from bs4 import BeautifulSoup

#To fetch the order details from the HTML files
directory_path = "D:\\grubhub\\grubhub plus"

with open('grubhub_plus.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Restaurant Name', 'Item Name', 'Quantity', 'Price', 'Subtotal', 'Delivery Fee', 'Taxes & Other Fees', 'Total'])

    for filename in os.listdir(directory_path):
        if filename.endswith(".html"):
            file_path = os.path.join(directory_path, filename)

            with open(file_path, 'r', encoding='utf-8') as html_file:
                html_content = html_file.read()

            soup = BeautifulSoup(html_content, "html.parser")

            restaurant_name_tag = soup.select_one("h4[data-testid='cart-restaurant-name']")
            restaurant_name = restaurant_name_tag.text if restaurant_name_tag else "Not Found"

            delivery_fee_tag = soup.select_one("div[data-testid='cart-line-item-delivery'] .lineItem-amount")
            delivery_fee = float(delivery_fee_tag.text.strip().strip('$').split('$')[-1]) if delivery_fee_tag else 0.0

            # Extract taxes and fees
            taxes_fees_tag = soup.select_one("div[data-testid='cart-line-item-tax_and_fees'] .lineItem-amount")
            taxes_and_fees = float(taxes_fees_tag.text.strip().strip('$').split('$')[-1]) if taxes_fees_tag else 0.0

            # Extract driver benefits fee
            driver_benefits_fee_tag = soup.select_one("div[data-testid='cart-line-item-driver_benefits_fee'] .lineItem-amount")
            driver_benefits_fee = float(driver_benefits_fee_tag.text.strip().strip('$').split('$')[-1]) if driver_benefits_fee_tag else 0.0

            # Sum the taxes and fees with the driver benefits fee
            total_taxes_and_fees = taxes_and_fees + driver_benefits_fee

            # Initialize total calculations for each file
            total_subtotal = 0.0

            # First loop to calculate subtotal of all items in order
            items = soup.select("span[data-testid='order-item']")
            for item in items:
                item_price_tag = item.select_one("span[class='s-col-md-6 u-text-right orderItem-price']")
                item_price = float(item_price_tag.text.strip().strip('$').split('$')[-1]) if item_price_tag else 0.0
                
                item_quantity_tag = item.select_one("div[data-testid='order-item-quantity']")
                item_quantity = int(item_quantity_tag.text.strip()) if item_quantity_tag else 1
                
                total_subtotal += item_price * item_quantity

            # Calculate total for the order
            total_order = total_subtotal + delivery_fee + total_taxes_and_fees

            # Second loop to write each item with the total order value and the same subtotal for each item
            for item in items:
                item_name_tag = item.select_one("div[data-testid='order-item-name']")
                item_name = item_name_tag.text.strip() if item_name_tag else "Not Found"

                item_price_tag = item.select_one("span[class='s-col-md-6 u-text-right orderItem-price']")
                item_price = float(item_price_tag.text.strip().strip('$').split('$')[-1]) if item_price_tag else 0.0
                
                item_quantity_tag = item.select_one("div[data-testid='order-item-quantity']")
                item_quantity = int(item_quantity_tag.text.strip()) if item_quantity_tag else 1

                item_subtotal = item_price * item_quantity
                
                writer.writerow([restaurant_name, item_name, item_quantity, f"${item_price:.2f}", f"${total_subtotal:.2f}", f"${delivery_fee:.2f}", f"${total_taxes_and_fees:.2f}", f"${total_order:.2f}"])

            # Output the processed file name
            print(f"Processed: {filename}")

print("All data extracted and saved to grubhub_plus.csv")
