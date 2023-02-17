import asyncio
import aiohttp
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Form
import pprint
import time
import requests
from fastapi import Request
from bs4 import BeautifulSoup
from fastapi import FastAPI
from BDalchemy import view_prices, save_prices

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.post('/natureexpressprices')
def prices():
    """API endpoint для получения цен на масла"""
    return get_nature_express_prices()

@app.get('/', response_class=HTMLResponse)
@app.get('/entry', response_class=HTMLResponse)
async def view(request: Request):
    """
    Начальная страица.
    API endpoint для получения сохраненных цен на масла.
    response_class=HTMLResponse указывает,
    что возвращаемое значение - HTML-страница
    """
    context = {"request": request, 'title': "Начальная страница"}
    return templates.TemplateResponse('entry.html', context)


@app.post('/viewprices', response_class=HTMLResponse)
async def view(
        request: Request,
        site: str = Form(default=None),
        oil_name: str = Form(default=None),
        price: float = Form(default=None),
        max_price: float = Form(default=None),
        start_date: str = Form(default=None),
        end_date: str = Form(default=None),):
    """
    API endpoint для получения сохраненных цен на масла.
    response_class=HTMLResponse указывает,
    что возвращаемое значение - HTML-страница
    """
    print(f'price =n {price}')
    prices = view_prices(
        site=site,
        oil_name=oil_name,
        price=price,
        max_price=max_price,
        start_date=start_date,
        end_date=end_date, )
    return templates.TemplateResponse('prices.html', {'request': request, 'prices': prices})



def get_nature_express_prices():
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
    """Получаем страницу сайта"""
    page = requests.get(prefix_url, timeout=5, headers=headers_chrome)
    """парсим страницу"""
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
        oil_name = soup.find('h1', class_="pagetitle", itemprop="name").text.strip()
        oir_price = soup.find('div', class_="product-price-wrapper").find('span', class_="",
                                                                          itemprop='price').text.rstrip().replace(' ₽', '')

        oil_name_prices[oil_name] = oir_price
        pprint.pprint(f'{url} | {oil_name} | {oil_name_prices[oil_name]}')
    if len(urls) == len(oil_name_prices):
        print('количество ссылок равно количеству запросов')
    else:
        print('Количество ссылок не равно количеству запросов')
    save_prices(oil_name_prices)
    return oil_name_prices


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
