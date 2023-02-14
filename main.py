import pprint
import time
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from BDalchemy import view_prices


app = FastAPI()


@app.get('/')
def prices():
    return get_prices()

@app.get('/viewprices')
def view():
    return view_prices()


def get_prices():
    headers_chrome = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
    headers_mozila = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }
    prefix_url = 'https://naturexpress.ru/katalog-tovarov/produktyi/rastitelnyie-masla/'
    address_site = 'https://naturexpress.ru/'
    page = requests.get(prefix_url, timeout=5, headers=headers_chrome)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a')
    urls = []
    for link in links:
        link_str = str(link.get('href'))
        if link_str.endswith('-ml'):
            urls.append(link_str)
    oil_name_prices = {}
    for url in urls:
        time.sleep(1)
        page = requests.get(f'{address_site}{url}', timeout=5, headers=headers_mozila)
        soup = BeautifulSoup(page.content, 'html.parser')
        """
        Если необходимо получать данные из списка продуктов,
        не обращаясь к каждому продукту, использовать этот код:
        a_absolute = soup.find("div", class_="col-xs-6 col-sm-4").find('a', class_='absolute', href=True)['href'].find('rastitelnyie-masla')
        print(a_absolute)
        if a_absolute > 0:
            oil_name = soup.find("div", class_="col-xs-6 col-sm-4").find('div', class_='title-h6').text.rstrip()
            oil_name_prices[oil_name] = float(soup.find("div", class_="col-xs-6 col-sm-4").find('div', class_='price').text.strip().replace(' ', '').replace('₽', ''))
            pprint.pprint(f'{url} | {oil_name} | {oil_name_prices[oil_name]}')
        else:
        """
        oil_name = soup.find('h1', class_="pagetitle", itemprop="name").text.strip()
        oir_price = soup.find('div', class_="product-price-wrapper").find('span', class_="",  itemprop='price').text.rstrip().replace(' ₽', '')
        oil_name_prices[oil_name] = oir_price
        #pprint.pprint(f'{url} | {oil_name} | {oil_name_prices[oil_name]}')
    if len(urls) == len(oil_name_prices):
        print('количество ссылок равно количеству запросов')
    else:
        print('Количество ссылок не равно количеству запросов')
    #save_prices(oil_name_prices)
    #return '\n'.join(f'{k}:{v}' for k, v in oil_name_prices.items())


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)

"""
https://naturexpress.ru/katalog-tovarov/produktyi/rastitelnyie-masla/amarantovoe-maslo-xolodnogo-otzhima-syirodavlennoe-50-ml
https://naturexpress.ru/katalog-tovarov/produktyi/rastitelnyie-masla/maslo-chyornogo-tmina-250-ml
https://naturexpress.ru/katalog-tovarov/produktyi/rastitelnyie-masla/maslo-chyornogo-tmina-250-ml
"""