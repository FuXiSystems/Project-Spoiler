__author__ = 'Mohamed'

from app.models.model import Model

from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, DateTime,String


class Exchanges(Model):
    __tablename__ = 'exchanges'

    id = Column(Integer, primary_key=True , nullable=False)
    name = Column(String(255), unique=True , nullable=True)
    title = Column(String(255), nullable=True)
    nickname = Column(String(50), nullable=True)
    symbol = Column(String(50), nullable=True)
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=True)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=True)
    effective_from = Column(DateTime, nullable=True)
    effective_to = Column(DateTime, nullable=True)

    currency = relationship("Currencies")
    country = relationship("Countries")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'nickname': self.nickname,
            'symbol': self.symbol,
            'currency_id': self.currency_id,
            'country_id': self.country_id,
            'effective_from': self.effective_from,
            'effective_to': self.effective_to
        }


    def __repr__(self):
        return self.name