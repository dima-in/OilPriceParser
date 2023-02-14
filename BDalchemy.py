from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://oilsquiser:oilsquiserpasswd@localhost/prices_parsinDB')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class OilPrice(Base):
    __tablename__ = 'oil_prices'

    id = Column(Integer, primary_key=True)
    site = Column(String(100))
    oil_name = Column(String(100))
    price = Column(Float)
    date = Column(Date)


def save_prices(dict_prices):
    for oil_name, price in dict_prices.items():
        price = OilPrice(site='nature-express', oil_name=oil_name, price=price, date=datetime.now())
        session.add(price)
        session.commit()


def view_prices(site=None, oil_name=None, price=None, max_price=None, start_date=None, end_date=None):
    filtered_query = session.query(OilPrice)
    if site:
        self_query = filtered_query.filter(OilPrice.site == site)
    if oil_name:
        self_query = filtered_query.filter(OilPrice.oil_name == oil_name)
    if price:
        self_query = filtered_query.filter(OilPrice.price == price)
    if max_price:
        self_query = filtered_query.filter(OilPrice.price <= max_price)
    if start_date:
        self_query = filtered_query.filter(OilPrice.date >= start_date)
    if end_date:
        self_query = filtered_query.filter(OilPrice.date <= end_date)
    return self_query.all()


