from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import random

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument(f'--proxy-server=https://proxy.cors.sh/{url}/sold')
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()



def random_sleep(minimum, maximum):
    time.sleep(random.uniform(minimum, maximum))



def get_price(product_url):
    driver.get(product_url+"?crt=1")
    soup = BeautifulSoup(driver.page_source)
    price_tag = soup.find('p', {'class': 'wt-text-title-larger wt-mr-xs-1'})
    try:
        price = price_tag.text.strip()
        price = re.findall(r'\d+', price)
        price = ' '.join(price)
    except:
        price = "eror"
    return price

def get_page_data(page, url):
    driver.get(f"{url}/sold??ref=pagination&page={page}")
    soup = BeautifulSoup(driver.page_source, 'lxml')
    with open("data.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
    productdata=[]
    productlist = soup.select('div.js-merch-stash-check-listing.v2-listing-card.wt-position-relative.wt-grid__item-xs-6.wt-flex-shrink-xs-1.wt-grid__item-xl-3.wt-grid__item-lg-4.wt-grid__item-md-4.listing-card-experimental-style')
    all_links = []
    for div in productlist:
        try:
            link_div = div.find('div', class_='v2-listing-card__info')
            plink = link_div.find('a').get('href')
        except:
            plink = div.select_one('a.listing-link')['href']
        all_links.append(plink)
    for index, div in enumerate(productlist):
        plink = all_links[index]
        # price = get_price(plink)
        product_name =  div.find('div',class_='v2-listing-card__info').find('h3').text.strip()
        products = {    
            "Shop Name":  url.split("/")[4],
            "Product Name": product_name,
            # "Price": price,
            "Frequency": 1,
            "Product urls": plink,
        }
        productdata.append(products)
    return productdata 




def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers',
        'x-requested-with': 'xhr',
        "x-cors-api-key": 'live_817ed3e527e8bf3d732be35c373371979933c782c6e8a84617bfe6e414646066',
                # Requests doesn't support trailers
                # 'TE': 'trailers',
    }
    shopdf = pd.read_excel('shops.xlsx')
    shopurl = shopdf.iloc[:, 0]
    totaldata = []
    for url in shopurl:
        driver.get(f"{url}/sold")
        sohpsoup = BeautifulSoup(driver.page_source,  'lxml')
        try:
            last_page_link = sohpsoup.find_all('li', {'class': ['btn', 'btn-list-item', 'btn-secondary', 'btn-group-item-md', 'hide-xs', 'hide-sm', 'hide-md']})[-2]
            last_page_number = int(last_page_link.find('a').get('data-page')) if last_page_link else None
        except:
            last_page_number = 1
        pagecount = 0
        for page in range(1, last_page_number + 1):
            data =  get_page_data(str(page), url)
            totaldata.extend(data)
            shopname = url.split("/")[4]
            print(data)
            print(f"Page {page} done for {shopname} removing duplicates increase frequncy and saving to excel")
            backupdf = pd.DataFrame(totaldata)
            backupdf['Frequency'] = backupdf.groupby('Product Name')['Frequency'].transform('sum')
            backupdf = backupdf.drop_duplicates(subset='Product Name')
            backupdf.to_excel("Backup.xlsx", index=False)
            totaldata = backupdf.to_dict('records')
            if pagecount == 5 :
                print("Sleeping for 1, 15 seconds")
                time.sleep(random.randint(3, 15)) 
                print("awake again fecthing data....")
                pagecount = 0
            pagecount += 1
            time.sleep(random.randint(1, 12)) 
    df = pd.DataFrame(totaldata)
    df.to_excel("output.xlsx", index=False)
    
main()
