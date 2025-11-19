import json
import time
import os
from utils import *
from SendTelegramMessage import send_telegram_message
import asyncio

sended_offers = []
closed_offers = []

def check_sended_and_actual_difference(item, sended_offers):
    for sended_item in sended_offers:
        if item['url'] == sended_item['url']:
            # check if price or time or estimated price changed
            if item['price'] != sended_item['price'] or item['reserve_price'] != sended_item['reserve_price']:
                return True
            else:
                return False
    return False

def get_good_offer(items):
    good_offers = []
    offers_updated = []
    closing_soon_offers = []
    for item in items:
        # in estimated price, remove the \xa0
        if item['estimated_price'] != 'No estimated price':
            item['estimated_price'] = item['estimated_price'].replace('\xa0', '')
    
    i = 0
    while i < len(items):
        if items[i]['estimated_price'] != 'No estimated price' and (items[i]['reserve_price'] == "Reserve price reached" or items[i]['reserve_price'] == "No reserve price") and items[i]['price'] != 'No price' and items[i]['time'] != 'No time':
            price = items[i]['price'].replace(' €', '')
            price = price.replace('\xa0', '')
            price = float(price)
            time_var = items[i]['time']
            pull_time = items[i]['pull_time']
            time_in_seconds = get_total_seconds(time_var)
            remaining_time = get_difference_with_pull_time(pull_time, time_var)
            high, low = items[i]['estimated_price'].split(' - ')
            high = high.replace(' €', '')
            low = low.replace(' €', '')
            try:
                high = float(high)
                low = float(low)
                median = (high + low) / 2
            except:
                print("Error converting to float")
                print(f"High: {high}")
                print(f"Low: {low}")
                print(items[i])
                i += 1
                continue
            
            if price < median * PERCENTAGE_THRESHOLD and remaining_time < REMAINING_TIME_THRESHOLD:
                # print(f"Price is 20% lower than the median and less than 30 minutes remaining")
                sended_offer_urls = [offer['url'] for offer in sended_offers]
                if items[i]['url'] not in sended_offer_urls and remaining_time > 0:
                    good_offers.append(items[i])
                    sended_offers.append(items[i])
                elif check_sended_and_actual_difference(items[i], sended_offers) and remaining_time > 0:
                    offers_updated.append(items[i])
                    print("Offer already sent")
                    for index, sended_item in enumerate(sended_offers):
                        if items[i]['url'] == sended_item['url']:
                            sended_offers[index] = items[i]
                            break
                    print("Offer updated")
                elif remaining_time < 90 and remaining_time > 0:
                    closed_offers_urls = [offer['url'] for offer in closed_offers]
                    if items[i]['url'] not in closed_offers_urls:
                        closing_soon_offers.append(items[i])
                        closed_offers.append(items[i])
        i += 1
    return good_offers, offers_updated, closing_soon_offers

while True:
    error = False
    with open('items.json', 'r') as f:
        try:
            items = json.load(f)
        except json.JSONDecodeError:
            error = True
        # if error is True, wait 1 second and try again
        if error:
            print("Error loading items.json, retrying...")
            time.sleep(0.25)
            continue
    items = sorted(items, key=lambda x: get_total_seconds(x['time']))
    good_offers, offers_updated, closing_soon_offers = get_good_offer(items)
    if len(good_offers) > 0:
        print("Good offers found:")
        for offer in good_offers:
            pull_time = offer['pull_time']
            time_var = offer['time']
            remaining_time = get_difference_with_pull_time(pull_time, time_var)
            # convert remainin time to  hours, minutes and seconds
            temp = remaining_time
            minutes = temp // 60
            seconds = temp % 60
            remaining_time_str = f"{int(minutes)}m {int(seconds)}s"
            message = "NEW OFFER FOUND:\n\n"
            for key, value in offer.items():
                if key == 'pull_time':
                    continue
                if key == 'time':
                    message += f"{key} : {remaining_time_str}\n"
                    print(f"{key} : {remaining_time_str}")
                    continue
                message += f"{key} : {value}\n"
                print(f"{key} : {value}")
            asyncio.run(send_telegram_message(message))
            print("\n")
            time.sleep(0.25)
    if len(offers_updated) > 0:
        print("Updated offers found:")
        for offer in offers_updated:
            pull_time = offer['pull_time']
            time_var = offer['time']
            remaining_time = get_difference_with_pull_time(pull_time, time_var)
            # convert remainin time to  hours, minutes and seconds
            temp = remaining_time
            minutes = temp // 60
            seconds = temp % 60
            remaining_time_str = f"{int(minutes)}m {int(seconds)}s"
            message = "OFFER UPDATED:\n\n"
            for key, value in offer.items():
                if key == 'pull_time':
                    continue
                if key == 'time':
                    message += f"{key} : {remaining_time_str}\n"
                    print(f"{key} : {remaining_time_str}")
                    continue
                message += f"{key} : {value}\n"
                print(f"{key} : {value}")
            asyncio.run(send_telegram_message(message))
            print("\n")
            time.sleep(0.25)
    if len(closing_soon_offers) > 0:
        print("Closing soon offers found:")
        for offer in closing_soon_offers:
            pull_time = offer['pull_time']
            time_var = offer['time']
            remaining_time = get_difference_with_pull_time(pull_time, time_var)
            # convert remainin time to  hours, minutes and seconds
            temp = remaining_time
            minutes = temp // 60
            seconds = temp % 60
            remaining_time_str = f"{int(minutes)}m {int(seconds)}s"
            message = "OFFER CLOSING SOON:\n\n"
            for key, value in offer.items():
                if key == 'pull_time':
                    continue
                if key == 'time':
                    message += f"{key} : {remaining_time_str}\n"
                    print(f"{key} : {remaining_time_str}")
                    continue
                message += f"{key} : {value}\n"
                print(f"{key} : {value}")
            asyncio.run(send_telegram_message(message))
            print("\n")
            time.sleep(0.25)
    # check if file items.json was modified in the last 90 seconds
    time.sleep(0.5)
    while time.time() - os.path.getmtime('items.json') > 1:
        time.sleep(1)