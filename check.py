from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

proxies = [
    "http://167.99.185.219:8888",
    "http://134.122.123.227:3128",
    "http://66.225.254.16:80",
    "http://159.65.221.25:80",
    "http://32.223.6.94:80",
    "http://100.26.211.80:80",
    "http://5.161.121.221:3128",
    "http://172.245.159.177:80",
    "http://20.151.176.41:3128",
    "http://68.188.59.198:80",
    "http://66.228.35.207:8083",
    "http://199.119.74.239:33333",
    "http://50.122.86.118:80",
    "http://198.23.143.24:6969",
    "http://134.209.74.17:8733",
    "http://67.213.212.39:24894",
    "http://199.127.176.139:64312",
    "http://172.108.208.74:80",
    "http://148.72.158.147:44013",
    "http://50.171.32.228:80",
    "http://50.171.32.229:80",
    "http://50.171.32.226:80",
    "http://50.171.32.227:80",
    "http://50.171.32.224:80",
    "http://50.171.32.225:80",
    "http://50.171.32.222:80",
    "http://50.171.51.138:80",
    "http://50.171.32.231:80",
    "http://50.171.32.230:80",
    "http://50.168.163.182:80",
]


def check_proxy(proxy):
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
    chrome_options.add_argument(f'--proxy-server={proxy}')
    
    try:
        with webdriver.Chrome(options=chrome_options) as driver:
            driver.get("https://whatismyipaddress.com/")  # You can replace this URL with any valid website
            # Add additional checks or actions if needed
        print(f"Proxy {proxy} is valid.")
    except WebDriverException as e:
        print(f"Proxy {proxy} is invalid. Error: {e}")

def main():
    for proxy in proxies:
        check_proxy(proxy)

if __name__ == "__main__":
    main()