import requests
import csv

def extract_restaurant_details_from_api(url, api_key):
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    all_restaurants = []
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data. Status Code: {response.status_code}")
        return []

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not in JSON format.")
        return []

    total_pages = data.get('pager', {}).get('total_pages', 1)
    for page_num in range(1, total_pages + 1):
        page_url = f"{url}&pageNum={page_num}"
        response = requests.get(page_url, headers=headers)

        if response.status_code != 200:
            print(f"Unable to access API, status code: {response.status_code}")
            break

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("Error: Response is not in JSON format.")
            break

        if 'results' in data:
            results = data['results']
            if not results:
                break
            for restaurant in results:
                restaurant_info = {
                    'Name': restaurant.get('name', 'N/A'),
                    'Rating': restaurant.get('ratings', {}).get('rating_value', 'N/A'),
                    'Reviews': restaurant.get('ratings', {}).get('rating_count', 0),
                    'Delivery Time': restaurant.get('delivery_time_estimate', 'N/A')
                }
                all_restaurants.append(restaurant_info)
        else:
            print("No restaurant results found in the response.")
            break
    return all_restaurants

def save_to_csv(data, filename="ratings_reviews_delivery.csv"):
    keys = data[0].keys()
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

api_url = 'https://api-gtm.grubhub.com/restaurants/search/search_listing?orderMethod=delivery&locationMode=DELIVERY&facetSet=umamiV6&pageSize=36&hideHateos=true&searchMetrics=true&location=POINT(-121.74051667%2038.54490661)&geohash=9qc7m8zk277k&sorts=default&facet=rating%3A4.0&includeOffers=true&featureControl=fastTagBadges%3Atrue&sortSetId=umamiv3&sponsoredSize=3&countOmittingTimes=true'
api_key = ''   #put authorization token here

restaurants = extract_restaurant_details_from_api(api_url, api_key)
save_to_csv(restaurants)