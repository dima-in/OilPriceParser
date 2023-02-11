import pprint
import time
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from Url import Base, engine, save_prices

app = FastAPI()


@app.get('/')
def prices():
    prices = get_prices()
    return prices


def url_to_parse():
    url = 'https://naturexpress.ru/katalog-tovarov/produktyi/rastitelnyie-masla/'
    url2 = 'https://maslodel.zone/oblepihovoe_maslo'
    address = {'tmin': 'maslo-chyornogo-tmina-250-ml',
               'tikvennoe': 'tyikvennoe-maslo-250-ml',
               'konoplyanoe': 'konoplyanoe-maslo-250-ml',
               'lnyanoe': 'lnyanoe-maslo-xolodnogo-otzhima-syirodavlennoe-250-ml',
               'greczkogo-orexa': 'maslo-greczkogo-orexa-xolodnogo-otzhima-syirodavlennoe-250-ml',
               'rastoropshi': 'maslo-rastoropshi-xolodnogo-otzhima-syirodavlennoe-250-ml',
               'kunzhutnoe': 'kunzhutnoe-maslo-xolodnogo-otzhima-syirodavlennoe-250-ml',
               'podsolnechnoe': 'podsolnechnoe-maslo-xolodnogo-otzhima-syirodavlennoe-250-ml',
               'gorchichnoe': 'gorchichnoe-maslo-xolodnogo-otzhima-syirodavlennoe-250-ml',
               'kokosovoe': 'kokosovoe-maslo-xolodnogo-otzhima-syirodavlennoe-250-ml',
               'oblepixovoe': 'oblepixovoe-maslo-xolodnogo-otzhima-syirodavlennoe-100-ml'}

    url_dict = {key: url + addr for key, addr in address.items()}
    # print(f'это url_list: {url_dict[key]} ')
    return url_dict




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
    prefix_url = 'https://naturexpress.ru/katalog-tovarov/produktyi/rastitelnyie-masla'
    address_site = 'https://naturexpress.ru/'
    page = requests.get(prefix_url, timeout=5, headers=headers_chrome)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a')
    urls = []
    for link in links:
        #time.sleep(4)
        link_str = str(link.get('href'))
        if link_str.endswith('-ml'):
            if link_str not in urls:
                link_filter = link_str
                print(f'auto url https://{link_filter}')
                urls.append(link_filter)
    oil_name_prices = {}
    for url in urls:
        time.sleep(3)
        print(f' handmade url: {address_site}{url}')
        page = requests.get(f'{address_site}{url}', timeout=5, headers=headers_mozila)
        soup = BeautifulSoup(page.content, 'html.parser')
        oil_name = soup.find('div', class_='title-h6').text.strip()
        oil_name_prices[oil_name] = soup.find('div', class_="price").text.strip()
    pprint.pprint(oil_name_prices)
    save_prices(oil_name_prices)
    return '\n'.join(f'{k}:{v}' for k, v in oil_name_prices.items())


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
"""
https://naturexpress.ru/katalog-tovarov/produktyi/rastitelnyie-masla/amarantovoe-maslo-xolodnogo-otzhima-syirodavlennoe-50-ml
https://naturexpress.ru/katalog-tovarov/produktyi/rastitelnyie-masla/maslo-chyornogo-tmina-250-ml
https://naturexpress.ru/katalog-tovarov/produktyi/rastitelnyie-masla/maslo-chyornogo-tmina-250-ml
"""