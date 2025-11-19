import json
import time
from main import get_object_information
from utils import *

# get number of item that are 30% lower than the median price and have less than 2 days remaining
def get_item_to_check(items):
    items_to_check = []
    for item in items:
        # in estimated price, remove the \xa0
        if item['estimated_price'] != 'No estimated price':
            item['estimated_price'] = item['estimated_price'].replace('\xa0', '')

    # print the items
    i = 0
    while i < len(items):
        # print(f"Item {i+1}/{len(items)}")
        # print(items[i]['estimated_price'])
        if items[i]['estimated_price'] != 'No estimated price':
            # print(f"Estimated price: {items[i]['estimated_price'].split(' - ')}")
            high, low = items[i]['estimated_price'].split(' - ')
            high = high.replace(' €', '')
            low = low.replace(' €', '')
            try:
                high = float(high)
                low = float(low)
            except:
                print("Error converting to float")
                print(f"High: {high}")
                print(f"Low: {low}")
                print(items[i])
                i += 1
                continue
            # print(f"High: {high}")
            # print(f"Low: {low}")
            median = (high + low) / 2
            # print(f"Median: {median}")
            # print(f"price: {items[i]['price']}," + f" time: {items[i]['time']}")
            # check if price is 30% lower than the median and if remaining time is less than 2 days
            if items[i]['price'] != 'No price' and items[i]['time'] != 'No time':
                price = items[i]['price'].replace(' €', '')
                price = price.replace('\xa0', '')
                price = float(price)
                # print(f"Price: {price}")
                time_var = items[i]['time']
                pull_time = items[i]['pull_time']
                time_in_seconds = get_total_seconds(time_var)
                remaining_time = get_difference_with_pull_time(pull_time, time_var)
                # print(f"Remaining time: {remaining_time}")
                if remaining_time < 0:
                    i += 1
                    continue
                reserve_price = items[i]['reserve_price']
                # print(f"Time in seconds: {time_in_seconds}")
                # print(f"Remaining time: {remaining_time}")
                # print(f"Price: {price}, Median: {median}, Remaining time: {remaining_time}, Reserve price: {reserve_price}")
                if price < median * PERCENTAGE_THRESHOLD and remaining_time < 172800:
                    # print(f"Price is 20% lower than the median")
                    # print the countdown based on the remaining time converted to days, hours, minutes and seconds all rouded to the nearest integer
                    temp = remaining_time
                    temp2 = get_time_var_from_seconds(remaining_time)
                    days = temp // 86400
                    temp = temp % 86400
                    hours = temp // 3600
                    temp = temp % 3600
                    minutes = temp // 60
                    temp = temp % 60
                    seconds = temp
                    # print(f"Time remaining: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")
                    # print(f"Item: {items[i]}")
                    
                    # if time is less than 1 hours send a telegram message to the user with all info
                    if remaining_time < REMAINING_TIME_THRESHOLD:
                        # print(f"Time is less than 1 day")
                        # print(f"link: {items[i]['url']}")
                        # print(f"Time var: {time_var}")
                        # print(f"New time var: {temp2}")
                        # print(f"Time remaining: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")
                        items_to_check.append(items[i])
                else:
                    # print(f"Price is not 30% lower than the median")
                    pass
        i += 1
    return items_to_check

while True:
    with open('items.json', 'r') as f:
        items = json.load(f)
    items = sorted(items, key=lambda x: get_total_seconds(x['time']) if x['time'] != 'No time' else float('inf'))
    items_to_check = []
    while len(items_to_check) == 0:
        items_to_check = get_item_to_check(items)
        if len(items_to_check) == 0:
            print("No items to check, waiting 5 minutes")
            time.sleep(300)
    i = 0
    j = 0
    while i < len(items):
        if items[i]['url'] not in [item['url'] for item in items_to_check]:
            i += 1
            continue
        print(f"Item {j+1}/{len(items_to_check)}")
        item = get_object_information(items[i]['url'], False)
        if item:
            if item['estimated_price'] != 'No estimated price':
                item['estimated_price'] = item['estimated_price'].replace('\xa0', '')
            # get difference between the old item and the new item an print the new item with highlated differences
            for key, value in item.items():
                
                # print old: in red
                if items[i][key] != value and key != 'pull_time':
                    print(f"{key} : {value} " + f"\033[91m(old: {items[i][key]})\033[0m")
                else: 
                    print(f"{key} : {value}")
            print()
            # add the item with actual price to the items list at the place of the old item and remove the old item
            items[i] = item
            with open('items.json', 'w') as f:
                json.dump(items, f)
        elif not item:
            # remove the item if it is not found
            new_items = items.copy()
            with open('items.json', 'w') as f:
                json.dump(new_items, f)
        i += 1
        j += 1
    # break