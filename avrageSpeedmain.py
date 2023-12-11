

import requests, re
import pandas as pd
from bs4 import BeautifulSoup

def get_data(url):
    cookies = {
        'uaid': 'dugPSIO2WQ9DuMxRqEg5T6d_kw9jZACC1BLNmzC6Wqk0MTNFyUopxzyt3Dyy1Cu1yjGlLLfCIySsyNgyUTcxsVLXRKmWAQA.',
        'user_prefs': 'bJpwgCwePL3lqmPlglGKzriogWFjZACC1BLNmxBaKydaydMvSEknrzQnR0cpNU_X3UlJRyk0GCpiBKFwEbEMAA..',
        'fve': '1702111705.0',
        '_fbp': 'fb.1.1702111705102.9642053264653538',
        'exp_ebid': 'm=%2BMJvgTGAjDMD0LNJVNObiIDNonid06PVkZIpQ8YfQvQ%3D,v=hsp-q1QuE8w06w_NyE1F4LwtbzyxqX2q',
        'datadome': '',
        'ua': '531227642bc86f3b5fd7103a0c0b4fd6',
        'last_browse_page': '',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    params = {
        'crt': '1',
    }
    r = requests.get(
        url,
        params=params,
        cookies=cookies,
        headers=headers,
    )
    pricesoup = BeautifulSoup(r.text, 'html.parser')
    price_tag = pricesoup.find('p', {'class': 'wt-text-title-larger wt-mr-xs-1'})
    price = price_tag.text.strip()
    price = re.findall(r'\d+', price)
    price = ' '.join(price)
    return price

def get_page_data(page, url):
    cookies = {
        'uaid': 'dugPSIO2WQ9DuMxRqEg5T6d_kw9jZACC1BLNmzC6Wqk0MTNFyUopxzyt3Dyy1Cu1yjGlLLfCIySsyNgyUTcxsVLXRKmWAQA.',
        'user_prefs': 'bJpwgCwePL3lqmPlglGKzriogWFjZACC1BLNmxBaKydaydMvSEknrzQnR0cpNU_X3UlJRyk0GCpiBKFwEbEMAA..',
        'fve': '1702111705.0',
        '_fbp': 'fb.1.1702111705102.9642053264653538',
        'exp_ebid': 'm=%2BMJvgTGAjDMD0LNJVNObiIDNonid06PVkZIpQ8YfQvQ%3D,v=hsp-q1QuE8w06w_NyE1F4LwtbzyxqX2q',
        'datadome': '',
        'ua': '531227642bc86f3b5fd7103a0c0b4fd6',
        'gtm_deferred': '%5B%5D',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://www.etsy.com/shop/NivariaDesigns/sold',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    params = {
        'ref': 'pagination',
        'page': str(page),
    }
    url=url+"/sold"
    response = requests.get(url, params=params, cookies=cookies, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    pagedata = soup.find('div', class_='content')
    productlist = soup.select('div.js-merch-stash-check-listing.v2-listing-card.wt-position-relative.wt-grid__item-xs-6.wt-flex-shrink-xs-1.wt-grid__item-xl-3.wt-grid__item-lg-4.wt-grid__item-md-4.listing-card-experimental-style')
    productdata=[]
    product_frequency = {}
    for product in productlist:
        product_name =  product.find('div',class_='v2-listing-card__info').find('h3').text
        product_link = product.find('a').get('href')
        existing_product = next((item for item in productdata if item["Product Name"] == product_name), None)
        try:
            price = get_data(product_link)
            # print(product_link)
        except:
            continue
        if existing_product:
            # If product exists, increment frequency
            existing_product["Frequency"] += 1
        else:
            # If product doesn't exist, add to productdata and set frequency to 1
            product_frequency[product_name] = 1
            products = {
                "Shop Name":  url.split("/")[4],
                "Product Name": product_name,
                "Price": price,
                "Frequency": product_frequency[product_name],
                "Product urls": url
            }
            print(products)
            productdata.append(products)
            # Write the current row to the Excel file
            current_row_df = pd.DataFrame([products])
            excel_file_path = 'products.xlsx'
            try:
                existing_data = pd.read_excel(excel_file_path)
                updated_data = pd.concat([existing_data, current_row_df], ignore_index=True)
                updated_data.to_excel(excel_file_path, index=False)
            except FileNotFoundError:
                current_row_df.to_excel(excel_file_path, index=False)
        
        # products = {"Product Name": product_name.text.strip(), "Product Link": product_link, "Price": price}
        
        productdata.append(products)
    return productdata

cookies = {
    'uaid': 'dugPSIO2WQ9DuMxRqEg5T6d_kw9jZACC1BLNmzC6Wqk0MTNFyUopxzyt3Dyy1Cu1yjGlLLfCIySsyNgyUTcxsVLXRKmWAQA.',
    'user_prefs': 'bJpwgCwePL3lqmPlglGKzriogWFjZACC1BLNmxBaKydaydMvSEknrzQnR0cpNU_X3UlJRyk0GCpiBKFwEbEMAA..',
    'fve': '1702111705.0',
    '_fbp': 'fb.1.1702111705102.9642053264653538',
    'exp_ebid': 'm=%2BMJvgTGAjDMD0LNJVNObiIDNonid06PVkZIpQ8YfQvQ%3D,v=hsp-q1QuE8w06w_NyE1F4LwtbzyxqX2q',
    'datadome': '',
    'ua': '531227642bc86f3b5fd7103a0c0b4fd6',
    'last_browse_page': 'https%3A%2F%2Fwww.etsy.com%2Fshop%2FMattBuildsIt',
    'gtm_deferred': '%5B%5D',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

shopdf = pd.read_excel('shops.xlsx')
shopurl =shopdf.iloc[:, 0]
total_products=[]
for url in shopurl:
    sohpsoup = BeautifulSoup(requests.get(url+"/sold", cookies=cookies, headers=headers).text, 'html.parser')
    try:
        last_page_link = sohpsoup.find_all('li', {'class': ['btn', 'btn-list-item', 'btn-secondary', 'btn-group-item-md', 'hide-xs', 'hide-sm', 'hide-md']})[-2]
        last_page_number = int(last_page_link.find('a').get('data-page')) if last_page_link else None
    except:
        last_page_number = 1
    total_pages = last_page_number
    
    for page in range(1, total_pages+1):
        total_products.extend(get_page_data(page,url))

df = pd.DataFrame(total_products)
df.to_excel('productdata.xlsx', index=False)