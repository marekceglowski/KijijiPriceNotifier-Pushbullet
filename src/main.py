#!/usr/bin/env python3

import os
import argparse
import sys
import requests
from bs4 import BeautifulSoup
import time
import json

def print_error_and_exit(error_message):
    """Print error message and exit program.
    Args:
        error_message (str): Error message to print.
    """

    print("Error: " + error_message)
    sys.exit()

# Send the push/message to all devices connected to Pushbullet
def send_message(token, title, body, link):
    
    headers = {'Access-Token': token, 'Content-Type': 'application/json'}
    message = {'type': 'link', 'title': title, 'body': body, 'url': link}
    message = json.dumps(message)
    
    try:
        req = requests.post(url='https://api.pushbullet.com/v2/pushes', data=message, headers=headers, timeout=20)
    except requests.exceptions.Timeout:
        print('Request Timeout')
        pass
    except requests.exceptions.TooManyRedirects:
        print('Too many requests')
        pass
    except requests.exceptions.RequestException as e:
        print(e)
        pass

def parse_page(url):
    """Will parse the listings on a Kijiji search page.

    Args:
        url (str): Full URL of search.

    Returns:
        list: List of dictionaries containing information about each listing.
    """

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    listings = []

    # Loop throuhg all prices
    for offer in soup.findAll("div", {"class": "regular-ad"}): # Scan regular-ad class to avoid featured ads realted to Kijiji Ads
        
        current_listing_dict = {}

        # Parse title
        title_list = offer.find_all(href=True)[0].text.split(" ")
        title = [i for i in title_list if i]
        title = " ".join(title).rstrip().strip("\n").strip(" ")

        # Append title to dict
        current_listing_dict['title'] = title

        # Parse price
        price = "".join(offer.findAll("div", {"class": "price"})[0].text.split(" ")).rstrip().strip('\n')

        if '$' in price:
            price = price.split('$')[-1].replace(',','')

        # Append price to dict
        current_listing_dict['price'] = price
            
        # Parse link
        link = offer.find_all(href=True)[0]['href']

        # Append link to dict
        current_listing_dict['link'] = link

        # Append to global listings list
        listings.append(current_listing_dict)

    return listings


def start_price_check_loop(url, token, max_price):
    """Run price checker.

    Args:
        url (str): Full URL of search.
        token (str): Pushbullet token.
        max_price (float): Max price to compare against.
    """

    known_listing_list = []
    first_run = True # To avoid all the inital listings that match price req

    while True:

        if first_run:
            send_message(token, "Kijiji Price Alert", "Started watching for search {}".format(url), url)

        try:
            print("Scanning page")
            current_listings = parse_page(url)
            print("Done scanning page")
        except requests.exceptions.ConnectionError:
            print("Scanning page failed")
            continue
        
        for listing in current_listings:

            #print("DEBUG {} {} {}".format(listing['title'], listing['price'], listing['link']))

            # Check if in known listing list
            if listing['link'] in known_listing_list:
                break

            # Add to known listing list
            known_listing_list.append(listing['link'])

            # Check if first run
            if first_run:
                continue

            # Check price
            try:
                if listing['price'] == 'PleaseContact':
                    continue
                elif listing['price'] == 'Swap/Trade':
                    continue
                elif listing['price'] == 'Free':
                    continue
                elif listing['price'] == '':
                    # Some prices are empty
                    continue
                elif float(listing['price']) <= max_price: # Convert price to float since it is not a string
                    message = "Kijiji Listing Alert: {} listed at price {} ({})".format(listing['title'], listing['price'], "https://www.kijiji.ca" + listing['link'])
                    print(message) # UnicodeEncodeError
                    send_message(token, "Kijiji Price Alert", message, "https://www.kijiji.ca" + listing['link'])
            except ValueError:
                print("{} is not a valid float".format(listing['price']))
                continue


        print("Sleeping before scanning")
        first_run = False
        time.sleep(500)


def main():
    
    if len(sys.argv) > 1:
        # Parse the arguments passed

        parser = argparse.ArgumentParser(description='Get low prices on Kijiji')
        parser.add_argument('-u', '--url', help="Kijiji Search URL.", required=True)
        parser.add_argument('-t', '--token', help="Pushbullet token.", required=True)
        parser.add_argument('-m', '--max', help="Max price.", required=True)

        args = parser.parse_args()

        kijiji_url = args.url
        pushbullet_token = args.token
        max_price = args.max

    elif len(sys.argv) == 1:
        # No paramters passed, parse env vars

        kijiji_url = os.getenv('SEARCH_URL')
        pushbullet_token = os.getenv('PUSHBULLET_TOKEN')
        max_price = os.getenv('MAX_PRICE')

        if kijiji_url == None:
            print_error_and_exit("Kijiji URL environment variable not set.")
        elif pushbullet_token == None:
            print_error_and_exit("Telegram Token environment variable not set.")

    start_price_check_loop(kijiji_url, pushbullet_token, float(max_price))
    

if __name__ == "__main__":
    main()