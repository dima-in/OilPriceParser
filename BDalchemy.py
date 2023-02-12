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
