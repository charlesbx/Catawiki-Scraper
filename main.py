from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import time
import json

CHROME_BIN = "/usr/bin/chromium"       # ajuste si `which chromium` retourne autre chose
CHROMEDRIVER_BIN = "/usr/bin/chromedriver"

def get_object_links_with_scroll(base_url):
    first_page = True
    # headless option
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome()
    driver.get(base_url)
    time.sleep(0.05)
    links = set()
    last_height = driver.execute_script("return window.scrollY")
    
    while True:
        broke = False
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for link in soup.find_all('a', class_='c-lot-card'):
            links.add(link['href'])
            if len(links) > 300:
                broke = True
                break
        if broke:
            break

        driver.execute_script("window.scrollTo(0, window.scrollY + 500)")

        new_height = driver.execute_script("return window.scrollY")
        if new_height == last_height:
            links_var = soup.find_all('a', class_='c-button-template u-cursor-pointer c-button__container c-button--primary u-bgcolor-brand u-typography-h7 u-w-full')
            if len(links_var) == 0:
                break
            elif len(links_var) == 1 and first_page:
                first_page = False
                l = links_var[0]['href']
                l = "https://www.catawiki.com" + l
                driver.get(l)
                time.sleep(0.05)
            elif len(links_var) == 2:
                l = links_var[1]['href']
                l = "https://www.catawiki.com" + l
                driver.get(l)
                time.sleep(0.05)
            else:
                break
            new_height = driver.execute_script("return window.scrollY")
        last_height = new_height

    driver.quit()
    return list(links)

if __name__ == '__main__':
    base_url = 'https://www.catawiki.com/fr/c/333-montres?sort=bidding_end_desc&filters=909%255B%255D%3D60922%26909%255B%255D%3D60796%26909%255B%255D%3D60226%26909%255B%255D%3D60548%26909%255B%255D%3D60654%26909%255B%255D%3D61062%26909%255B%255D%3D61158%26909%255B%255D%3D60424%26909%255B%255D%3D60430%26909%255B%255D%3D60555%26909%255B%255D%3D60210%26909%255B%255D%3D60156%26909%255B%255D%3D60088%26seller_location%255B%255D%3Dfr%26seller_location%255B%255D%3Dtr%26seller_location%255B%255D%3Dnl%26seller_location%255B%255D%3Dit%26seller_location%255B%255D%3Dpl%26seller_location%255B%255D%3Dlt%26seller_location%255B%255D%3Des%26seller_location%255B%255D%3Dpt%26seller_location%255B%255D%3Dbe%26seller_location%255B%255D%3Dde%26seller_location%255B%255D%3Dse%26seller_location%255B%255D%3Dro%26seller_location%255B%255D%3Dat%26seller_location%255B%255D%3Dhu%26seller_location%255B%255D%3Dcz%26seller_location%255B%255D%3Dlv%26seller_location%255B%255D%3Dgr%26seller_location%255B%255D%3Dch%26seller_location%255B%255D%3Dgb%26object_type%255B%255D%3D18131%26object_type%255B%255D%3D18129%26object_type%255B%255D%3D18133'
    links = get_object_links_with_scroll(base_url)
    print(f"Nombre total de liens : {len(links)}")

count = 0
last_items = []
item_template = {
    "title": "",
    "price": "",
    "time": "",
    "url": "",
    "estimated_price": "",
    "pull_time": "",
    "reserve_price": "",
}

def get_object_information(link, isCounted=True, driver=None):
    global count, last_items, item_template
    if not driver:
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless=new')
        driver = webdriver.Chrome(options=options)
    driver.get(link)
    time.sleep(0.25)
    # WebDriverWait(driver, 3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time_obj = soup.find_all('time', class_='u-text-tabular-figures')
    # until soup.find_all('div', class_='LotBidStatusSection_subtitle-content__kkad5 LotBidStatusSection_visible__kj_F3 u-typography-h7 u-m-t-xs')
    # if there is no time object, load the link again
    count_retry = 0
    while len(time_obj) == 0:
        driver.get(link)
        time.sleep(0.75)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time_obj = soup.find_all('time', class_='u-text-tabular-figures')
        count_retry += 1
        if count_retry == 3:
            # skip the link if it fails to load
            break
    if len(time_obj) == 0:
        print("No time : ", link)
        driver.quit()
        return None

    title_obj = soup.find_all('h1')
    try:
        price_obj = soup.find_all('div', class_='LotBidStatusSection_bid-amount__bWWF4 u-typography-h2')
    except:
        print("No price")
        price_obj = None
    try:
        estimated_price_obj = soup.find_all('span', class_='u-no-wrap')
        
        price = estimated_price_obj[1].text
        if '€' not in price:
            raise Exception("No estimated price")

        low_estimated_price_obj1 = price.split(' - ')[0].replace(' € ', '') + ' €'
        high_estimated_price_obj1 = price.split(' - ')[1].replace(' € ', '') + ' €'
        
        print(low_estimated_price_obj1, high_estimated_price_obj1)
    except:
        low_estimated_price_obj1 = None
        high_estimated_price_obj1 = None
    print(link)
    try:
       time_var = time_obj[0].text.strip()
    except:
        time_var = "No time"
    
        
    title_var = title_obj[0].text
    try:
        price_var = price_obj[0].text.replace(' €', '') + ' €'
    except:
        price_var = "No price"
        print(price_obj)
    estimated_price_var = (low_estimated_price_obj1 + ' - ' + high_estimated_price_obj1) if low_estimated_price_obj1 and high_estimated_price_obj1 else "No estimated price"
    item = item_template.copy()
    item['time'] = time_var
    item['url'] = link
    item['title'] = title_var
    item['price'] = price_var
    item['estimated_price'] = estimated_price_var
    try:
        reserve_price_obj = soup.find_all('div', class_='LotBidStatusSection_subtitle-content__kkad5 LotBidStatusSection_visible__kj_F3 u-typography-h7 u-m-t-xs')
        print(reserve_price_obj)
        print(len(reserve_price_obj))
        if len(reserve_price_obj) > 0:
            item['reserve_price'] = reserve_price_obj[0].text
            if "Prix de réserve non atteint" in item['reserve_price']:
                item['reserve_price'] = "Reserve price not reached"
            elif "Sans prix de réserve" in item['reserve_price']:
                item['reserve_price'] = "No reserve price"
            else:
                item['reserve_price'] = "Reserve price reached"
        else:
            item['reserve_price'] = "No reserve price"
    except:
        item['reserve_price'] = "No reserve price"
    
    item['pull_time'] = time.time()
    
    if isCounted:
        print(f"Item number: {count}/{len(links)}")
    # for key, value in item.items():
    #     print(f"{key} : {value}")
    # print()
    driver.quit()
    return item
    

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    for link in links:
        # for each link open the page and time object with class u-text-tabular-figures
        count += 1
        item = get_object_information(link)
        if item:
            last_items.append(item)

    print(last_items)
    # sort items by time remaining (ascending)
    last_items = sorted(last_items, key=lambda x: x['time'])
    # save items to a file
    with open('items.json', 'w') as f:
        json.dump(last_items, f)