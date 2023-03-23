# zillow_scraper/extract.py
import time
import random
import requests
import datetime as dt
from bs4 import BeautifulSoup

tab_class_map = {
    'address': ('h1', 'Text-c11n-8-84-0__sc-aiai24-0 qxgaF'),
    'status': ('span', 'Text-c11n-8-84-0__sc-aiai24-0 dpf__sc-1yftt2a-1 qxgaF ixkFNb'),
    'zestimate': ('span', 'Text-c11n-8-84-0__sc-aiai24-0 eIEmla'),
    'overview': ('span', 'Text-c11n-8-84-0__sc-aiai24-0 dpf__sc-2arhs5-3 qxgaF kOlNqB'),
    'facts_and_features': ('li', 'ListItem-c11n-8-84-0__sc-10e22w8-0 kDUoZv'),
    'price_and_tax_history': ('td', 'hdp__sc-f00yqe-0 igpNxE'),
    'commute_time': ('span', 'Text-c11n-8-84-0__sc-aiai24-0 qxgaF'),
}


def extract_housing_info(url):
    '''
    :param url: Zillow house URL
    :return: a dictionary with fields of interest
    '''

    # Add headers and random sleep time to bypass robot test
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0)   Gecko/20100101 Firefox/78.0",
        "Referer": "https://www.google.com"
    }

    sleep_time = random.randint(10, 19) / 10
    time.sleep(sleep_time)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    housing_info = dict()
    for key in tab_class_map.keys():
        housing_info[key] = soup.find_all(tab_class_map.get(key)[0], class_=tab_class_map.get(key)[1])

    feature_info = dict()
    for feature in housing_info['facts_and_features']:
        text = feature.get_text(strip=True).split(':')
        if len(text) == 2:
            feature_info = {**feature_info, **dict([text])}

    return {
        # Extract information from the HTML using BeautifulSoup selectors
        # TODO: get listing date from price and tax history
        'Date': dt.datetime.strftime(dt.datetime.today().date(), '%m/%d/%Y'),
        'Address': housing_info['address'][0].get_text(strip=True),
        'URL': url,
        'Status': housing_info['status'][0].get_text(strip=True),
        'Region': feature_info.get('Region'),
        'Home type': feature_info.get('Home type', housing_info['overview'][0].get_text(strip=True)),
        'Year built': feature_info.get('Year built', housing_info['overview'][1].get_text(strip=True).split()[-1]),
        'List price': soup.find('span', {'data-testid': 'price'}).get_text(strip=True),
        'Zestimate': housing_info['zestimate'][0].get_text(strip=True),
        'Hoa': None,  # TODO: get HOA information
        'Square feet': soup.find_all('span', {'data-testid': 'bed-bath-item'})[2].find('strong').text,
        'Price/sqft': housing_info['overview'][6].get_text(strip=True).split()[0],
        'Bedrooms': soup.find_all('span', {'data-testid': 'bed-bath-item'})[0].find('strong').text,
        'Bathrooms': soup.find_all('span', {'data-testid': 'bed-bath-item'})[1].find('strong').text,
        'Cooling': feature_info.get('Cooling features', housing_info['overview'][3].get_text(strip=True)),
        'Heating': feature_info.get('Heating features', housing_info['overview'][2].get_text(strip=True)),
        'Total parking spaces': feature_info.get('Total spaces'),
        'Parking features': feature_info.get('Parking features'),
        'Attached garage': None,  # TODO: get attached_garage information
        'Garage spaces': feature_info.get('Garage spaces'),
        'Commute time': None,  # TODO: get commute_time information
        'Greatschools rating': None,  # TODO: get greatschools_rating information
        'Middle': None,  # TODO: get greatschools_rating information
        'High': None,  # TODO: get greatschools_rating information
        'Architectural style': feature_info.get('Architectural style'),
        'Lot size': feature_info.get('Lot size'),
        'Lot features': feature_info.get('Lot features'),
        'Exterior features': feature_info.get('Exterior features'),
        'Patio and porch details': feature_info.get('Patio and porch details'),
        'Fencing': feature_info.get('Fencing'),
        'Annual tax amount': feature_info.get('Annual tax amount'),
        'Interior': feature_info.get('Interior'),
        'Property condition': feature_info.get('Property condition'),
        'New construction': feature_info.get('New construction'),
        'Property': feature_info.get('Property'),
        'HOA and financial': feature_info.get('HOA and financial'),
        'Tax assessed value': feature_info.get('Tax assessed value'),
        'Listing terms': feature_info.get('Listing terms'),
        "Buyer's agent fee": feature_info.get("Buyer's agent fee",
                                              f"{housing_info['overview'][7].get_text(strip=True).split('%')[0]}%"),
        'Offer review date': feature_info.get('Offer review date'),
        'Rent Zestimate': feature_info.get('Rent Zestimate'),
        'Community and neighborhood': feature_info.get('Community and neighborhood'),
        'Walk Score®': None,  # TODO: get walk_score information
        'Transit Score™': None,  # TODO: get transit_score information
        'Basement': feature_info.get('Basement'),
        'Laundry': feature_info.get('Laundry features'),
        'Fireplaces': feature_info.get('Fireplace features'),
    }
