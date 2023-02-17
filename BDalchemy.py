import asyncio
import aiohttp
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



"""создаем базовый класс"""
Base = declarative_base()

"""создаем соеденение с базой данных"""
engine = create_engine('mysql+mysqlconnector://oilsquiser:oilsquiserpasswd@localhost/prices_parsinDB')

"""создаем таблицу в базе данных"""
Base.metadata.create_all(engine)

"""создаем сессию для работы с базой данных"""
Session = sessionmaker(bind=engine)
session = Session()

"""создаем класс для модели данных"""


class OilPrice(Base):
    __tablename__ = 'oil_prices'
    id = Column(Integer, primary_key=True)
    site = Column(String(100))
    oil_name = Column(String(100))
    price = Column(Float)
    date = Column(Date)


async def save_prices(dict_prices):
    """Функция для сохранения цен в базе данных"""
    with Session() as session:
        for oil_name, price in dict_prices.items():
            price = OilPrice(site='nature-express', oil_name=oil_name, price=price, date=datetime.now())
            session.add(price)
            session.commit()


def view_prices(
                site: str = None,
                oil_name: str = None,
                price: float = None,
                max_price: float = None,
                start_date: str = None,
                end_date: str = None):
    """Функция для просмотра цен в базе данных"""
    with Session() as session:
        query = session.query(OilPrice)
        """
        Проверка is not Nonе используется, чтобы избежать
        интерпетации значения 0 как False.
        filter_by фильтрует записи по конкретным значениям атрибутов
        filter подходит для более сложной фильтрации
        """

        if site is not None:
            query = query.filter_by(site=site)
        if oil_name is not None:
            query = query.filter(OilPrice.oil_name.ilike(f'%{oil_name}%'))
        if price is not None:
            query = query.filter_by(price=price)
        if max_price is not None:
            query = query.filter(OilPrice.price <= max_price)
        if start_date is not None:
            query = query.filter(OilPrice.date >= start_date)
        if end_date is not None:
            query = query.filter(OilPrice.date <= end_date)
        print(f"in view_prices oil_name = {oil_name}")
        print(f"in view_prices site = {site}")
        prices = query.all()
        return prices
