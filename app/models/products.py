__author__ = 'Mohamed'
from app.models.model import Model

from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, DateTime,String

class Products(Model):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True , nullable=False)
    exchange_id = Column(Integer, ForeignKey('exchanges.id'), nullable=True)
    instrument_id = Column(Integer, ForeignKey('instruments.id'), nullable=True)
    name = Column(String(255), unique=True , nullable=True)
    title = Column(String(255), nullable=True)
    symbol = Column(String(50), nullable=True)
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=True)
    effective_from = Column(DateTime, nullable=True)
    effective_to = Column(DateTime, nullable=True)

    instrument = relationship("Instruments")
    currency = relationship("Currencies")
    exchange = relationship("Exchanges")

    def serialize(self):
        return {
            'id': self.id,
            'exchange_id': self.exchange_id,
            'instrument_id': self.instrument_id,
            'name': self.name,
            'title': self.title,
            'symbol': self.symbol,
            'currency_id': self.currency_id,
            'effective_from': self.effective_from,
            'effective_to': self.effective_to
        }


    def __repr__(self):
        return self.name
