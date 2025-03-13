import requests
import csv

def extract_restaurant_details_from_api(url, api_key, output_csv):
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    all_restaurants = []
    response = requests.get(url, headers=headers)
    data = response.json()
    total_pages = data['pager']['total_pages']

    for page_num in range(1, total_pages + 1):
        page_url = f"{url}&pageNum={page_num}"
        response = requests.get(page_url, headers=headers)
        if response.status_code != 200:
            print(f"Unable to access API, status code: {response.status_code}")
            break
        data = response.json()

        if 'results' in data:
            results = data['results']
            if not results:
                break
            for restaurant in results:
                restaurant_info = {
                    'name': restaurant.get('name', 'N/A'),
                    'address': f"{restaurant['address'].get('street_address', '')}, {restaurant['address'].get('address_locality', '')}, {restaurant['address'].get('address_region', '')}, {restaurant['address'].get('postal_code', '')}",
                    'phone_number': f"{restaurant['phone_number'].get('country_code', '')} {restaurant['phone_number'].get('phone_number', '')}",
                    'cuisines': ', '.join(restaurant.get('cuisines', []))
                }
                all_restaurants.append(restaurant_info)
        else:
            print("No restaurant results found.")
            break

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'address', 'phone_number', 'cuisines'])
        writer.writeheader()
        writer.writerows(all_restaurants)
    return all_restaurants

api_url = 'https://api-gtm.grubhub.com/restaurants/search/search_listing?orderMethod=delivery&locationMode=DELIVERY&facetSet=umamiV6&pageSize=36&hideHateos=true&searchMetrics=true&location=POINT(-121.74051667%2038.54490661)&geohash=9qc7m8zk277k&sorts=default&facet=rating%3A4.0&includeOffers=true&featureControl=fastTagBadges%3Atrue&sortSetId=umamiv3&sponsoredSize=3&countOmittingTimes=true'
api_key = ''     #put authorization token here
output_csv = 'restaurants_details.csv'
restaurants = extract_restaurant_details_from_api(api_url, api_key, output_csv)

