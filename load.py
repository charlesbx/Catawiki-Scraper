import json
import time
from utils import *

if __name__ == '__main__':
    items_closing = []

    # open the file and load the items
    with open('items.json', 'r') as f:
        items = json.load(f)

    for item in items:
        # in estimated price, remove the \xa0
        if item['estimated_price'] != 'No estimated price':
            item['estimated_price'] = item['estimated_price'].replace('\xa0', '')

    # print the items
    for item in items:
        if item['estimated_price'] != 'No estimated price':
            # print(f"Estimated price: {item['estimated_price'].split(' - ')}")
            high, low = item['estimated_price'].split(' - ')
            high = high.replace(' €', '')
            low = low.replace(' €', '')
            try:
                high = float(high)
                low = float(low)
            except:
                print("Error converting to float")
                print(f"High: {high}")
                print(f"Low: {low}")
                print(item)
                continue
            # print(f"High: {high}")
            # print(f"Low: {low}")
            median = (high + low) / 2
            # print(f"Median: {median}")
                
            # check if price is 30% lower than the median and if remaining time is less than 2 days
            if item['price'] != 'No price' and item['time'] != 'No time':
                price = item['price'].replace(' €', '')
                price = price.replace('\xa0', '')
                price = float(price)
                # print(f"Price: {price}")
                time_var = item['time']
                pull_time = item['pull_time']
                time_in_seconds = get_total_seconds(time_var)
                remaining_time = get_difference_with_pull_time(pull_time, time_var)
                if remaining_time < 0:
                    continue
                new_time_var = get_time_var_from_seconds(remaining_time)
                reserve_price = item['reserve_price']
                # print(f"Time in seconds: {time_in_seconds}")
                if price < median * 0.70 and remaining_time < 172800 and reserve_price != 'Reserve price not reached':
                    # print(f"Price is 30% lower than the median")
                    # print the countdown based on the remaining time converted to days, hours, minutes and seconds all rouded to the nearest integer
                    temp = remaining_time
                    days = temp // 86400
                    temp = temp % 86400
                    hours = temp // 3600
                    temp = temp % 3600
                    minutes = temp // 60
                    temp = temp % 60
                    seconds = temp
                    # print(f"Time remaining: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")
                    # print(f"Item: {item}")
                    
                    # if time is less than 1 day send a telegram message to the user with all info
                    if remaining_time < 43200*2:
                        # print(f"Time is less than 1 day")
                        # change the time to the new time
                        item['time'] = new_time_var
                        items_closing.append(item)
                else:
                    # print(f"Price is not 30% lower than the median")
                    pass

    # sort the items by time
    items_closing = sorted(items_closing, key=lambda x: x['pull_time'])

    for item in items_closing:
        for key in item:
            print(f"{key}: {item[key]}")
        print("\n")