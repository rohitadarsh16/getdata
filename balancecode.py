import aiohttp
import asyncio
import random
import nest_asyncio
import pandas as pd
import re
from bs4 import BeautifulSoup
async def fetch(session, url,cookies=None,headers=None, params=None):
    async with session.get(url,cookies=cookies ,headers=headers, params=params) as response:
        return await response.text()
    
async def fetch_product_data(session, product_url):
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
         'x-requested-with': 'xhr',
        "x-cors-api-key": 'live_817ed3e527e8bf3d732be35c373371979933c782c6e8a84617bfe6e414646066',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    params = {
        'crt': '1',
    }
    response = await fetch(session, "https://proxy.cors.sh/"+product_url,  cookies=cookies, headers=headers,params=params)
    soup = BeautifulSoup(response, 'html.parser')
    price_tag = soup.find('p', {'class': 'wt-text-title-larger wt-mr-xs-1'})
    try:
        price = price_tag.text.strip()
        price = re.findall(r'\d+', price)
        price = ' '.join(price)
    except:
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(response)
        price = "eror"
    return price


async def random_sleep(mintime, maxtime):
    await asyncio.sleep(random.randint(mintime, maxtime))

async def get_page_data(session,semaphore,page, url):
    async with semaphore:
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
            'Referer': '',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'x-requested-with': 'xhr',
            "x-cors-api-key": 'live_817ed3e527e8bf3d732be35c373371979933c782c6e8a84617bfe6e414646066',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        params = {
            'ref': 'pagination',
            'page': str(page),
        }
        # print(url)

        response = await fetch(session, f"https://proxy.cors.sh/{url}/sold",  cookies=cookies,headers=headers,params=params)
        soup = BeautifulSoup(response, 'html.parser')
        with open("index.html", "w", encoding="utf-8") as f:
                f.write(response)
        productdata=[]
        productlist = soup.select('div.js-merch-stash-check-listing.v2-listing-card.wt-position-relative.wt-grid__item-xs-6.wt-flex-shrink-xs-1.wt-grid__item-xl-3.wt-grid__item-lg-4.wt-grid__item-md-4.listing-card-experimental-style')
        # all_links_divs = soup.find_all('div', class_='v2-listing-card__info')
        all_links = []
        for div in productlist:
            try:
                link_div = div.find('div', class_='v2-listing-card__info')
                plink = link_div.find('a').get('href')
            except:
                plink = div.select_one('a.listing-link')['href']
            all_links.append(plink)
                
        
        
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_product_data(session, product_url) for product_url in all_links]
            results = await asyncio.gather(*tasks)
        product_frequency = {}

        for index, data in enumerate(productlist):
            product_name =  data.find('div',class_='v2-listing-card__info').find('h3').text.strip()
            product_url = all_links[index]
            product_price = results[index]

            # Check if product already exists in productdata
            existing_product = next((item for item in productdata if item["Product Name"] == product_name), None)

            if existing_product:
                # If product exists, increment frequency
                existing_product["Frequency"] += 1
            else:
                # If product doesn't exist, add to productdata and set frequency to 1
                product_frequency[product_name] = 1
                products = {
                    "Shop Name":  url.split("/")[4],
                    "Product Name": product_name,
                    "Price": product_price,
                    "Frequency": product_frequency[product_name],
                    "Product urls": product_url
                }
                productdata.append(products)
            await random_sleep(1,3)

        return productdata


async def main():
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
        'x-requested-with': 'xhr',
        "x-cors-api-key": 'live_817ed3e527e8bf3d732be35c373371979933c782c6e8a84617bfe6e414646066',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }
    
    shopdf = pd.read_excel('shops.xlsx')
    shopurl = shopdf.iloc[:, 0]
    totaldata = []
    semaphore = asyncio.Semaphore(5)  # Adjust the number of concurrent requests
    async with aiohttp.ClientSession() as session:
        for url in shopurl:
            shoplink= "https://proxy.cors.sh/"+url+"/sold"
            response = await fetch(session, shoplink, cookies=cookies, headers=headers)
            with open("output.html", "w", encoding="utf-8") as f:
                f.write(response)
            sohpsoup = BeautifulSoup(response, 'html.parser')
            try:
                last_page_link = sohpsoup.find_all('li', {'class': ['btn', 'btn-list-item', 'btn-secondary', 'btn-group-item-md', 'hide-xs', 'hide-sm', 'hide-md']})[-2]
                last_page_number = int(last_page_link.find('a').get('data-page')) if last_page_link else None
            except:
                last_page_number = 1
                
            tasks = [get_page_data(session, semaphore, page, url) for page in range(1, last_page_number + 1)]
            data = await asyncio.gather(*tasks)
            totaldata.extend(data)
    df = pd.DataFrame(totaldata)
    df.to_excel("output.xlsx", index=False)
if __name__ == "__main__":
    asyncio.run(main())
