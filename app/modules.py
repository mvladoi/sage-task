
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import Column, String, Integer, BigInteger, Float
from flask_marshmallow import Marshmallow


base = declarative_base()

class Transaction(base):  
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    symbol = Column(String)
    currency = Column(String)
    amount = Column(Float)
    date = Column(BigInteger)

    def __repr__(self):
        return "<User %r>" % self.username



       