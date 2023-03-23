# zillow_scraper/extract.py

import requests
from bs4 import BeautifulSoup

tab_class_map = {
    'address': ('h1', 'Text-c11n-8-84-0__sc-aiai24-0 qxgaF'),
    'status': ('span', 'Text-c11n-8-84-0__sc-aiai24-0 dpf__sc-1yftt2a-1 qxgaF ixkFNb'),
    'overview': ('span', 'Text-c11n-8-84-0__sc-aiai24-0 dpf__sc-2arhs5-3 qxgaF kOlNqB'),
    'facts_and_features': ('span', 'Text-c11n-8-84-0__sc-aiai24-0 qxgaF'),
    'price_and_tax_history': ('td', 'hdp__sc-f00yqe-0 igpNxE'),
    'commute_time': ('span', 'Text-c11n-8-84-0__sc-aiai24-0 qxgaF')
}


def extract_housing_info(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    housing_info = dict()
    for key in tab_class_map.keys():
        housing_info[key] = soup.find_all(tab_class_map.get(key)[0], class_=tab_class_map.get(key)[1])

    return {
        # Extract information from the HTML using BeautifulSoup selectors
        # 'date': housing_info['price_and_tax_history'][0].get_text(strip=True),
        'address': housing_info['address'][0].get_text(strip=True),
        'url': url,
        'status': housing_info['status'][0].get_text(strip=True),
        'region': soup.find('span', {'class':'.region-selector'}).text.strip(),
        'home_type': housing_info['overview'][0].get_text(strip=True),
        'year_built': housing_info['overview'][1].get_text(strip=True).split()[-1],
        'list_price': soup.find('span', {'data-testid': 'price'}).get_text(strip=True),
        'zestimate': soup.find('span', {'class':'.zestimate-selector'}).text.strip(),
        'hoa': soup.find('span', {'class':'.hoa-selector'}).text.strip(),
        'square_feet': soup.find_all('span', {'data-testid': 'bed-bath-item'})[2].find('strong').text,
        'price_per_sqft': housing_info['overview'][6].get_text(strip=True).split()[0],
        'bedrooms': soup.find_all('span', {'data-testid': 'bed-bath-item'})[0].find('strong').text,
        'bathrooms': soup.find_all('span', {'data-testid': 'bed-bath-item'})[1].find('strong').text,
        'cooling': housing_info['overview'][3].get_text(strip=True),
        'heating': housing_info['overview'][2].get_text(strip=True),
        'total_parking_spaces': soup.find('span', {'class':'.total-parking-spaces-selector'}).text.strip(),
        'parking_features': soup.find('span', {'class':'.parking-features-selector'}).text.strip(),
        'attached_garage': soup.find('span', {'class':'.attached-garage-selector'}).text.strip(),
        'garage_spaces': housing_info['overview'][4].get_text(strip=True),
        # 'commute_time': soup.find('span', {'class':'.commute-time-selector'}).text.strip(),
        'greatschools_rating': soup.find('span', {'class':'.greatschools-rating-selector'}).text.strip(),
        'architectural_style': soup.find('span', {'class':'.architectural-style-selector'}).text.strip(),
        'lot_size': housing_info['overview'][5].get_text(strip=True),
        'lot_features': soup.find('span', {'class':'.lot-features-selector'}).text.strip(),
        'exterior_features': soup.find('span', {'class':'.exterior-features-selector'}).text.strip(),
        'patio_and_porch_details': soup.find('span', {'class':'.patio-and-porch-details-selector'}).text.strip(),
        'fencing': soup.find('span', {'class':'.fencing-selector'}).text.strip(),
        'annual_tax_amount': soup.find('span', {'class':'.annual-tax-amount-selector'}).text.strip(),
        'see_more_interior': soup.find('span', {'class':'.see-more-interior-selector'}).text.strip(),
        'property_condition': soup.find('span', {'class':'.property-condition-selector'}).text.strip(),
        'new_construction': soup.find('span', {'class':'.new-construction-selector'}).text.strip(),
        'see_more_property': soup.find('span', {'class':'.see-more-property-selector'}).text.strip(),
        'hoa_and_financial': soup.find('span', {'class':'.hoa-and-financial-selector'}).text.strip(),
        'tax_assessed_value': soup.find('span', {'class':'.tax-assessed-value-selector'}).text.strip(),
        'listing_terms': soup.find('span', {'class':'.listing-terms-selector'}).text.strip(),
        'buyer_agent_fee': f"{housing_info['overview'][7].get_text(strip=True).split('%')[0]}%",
        'offer_review_date': soup.find('span', {'class':'.offer-review-date-selector'}).text.strip(),
        'rent_zestimate': soup.find('span', {'class':'.rent-zestimate-selector'}).text.strip(),
        'community_and_neighborhood': soup.find('span', {'class':'.community-and-neighborhood-selector'}).text.strip(),
        'walk_score': soup.find('span', {'class':'.walk-score-selector'}).text.strip(),
        'transit_score': soup.find('span', {'class':'.transit-score-selector'}).text.strip()
    }
