__author__ = 'Mohamed'

from app.models.model import Model
# from app.models.advisers import Adviser

from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, DateTime, Numeric

class HistoricQuote(Model):
    __tablename__ = 'historic_quotes'

    id = Column(Integer, primary_key=True , nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    latest_value = Column(Numeric(36,8), nullable=True)
    open = Column(Numeric(36,8), nullable=True)
    high = Column(Numeric(36,8), nullable=True)
    low = Column(Numeric(36,8), nullable=True)
    close = Column(Numeric(36,8), nullable=True)
    quote_date = Column(DateTime, nullable=True)
    effective_from = Column(DateTime, nullable=True)
    effective_to = Column(DateTime, nullable=True)

    product = relationship("Products")

    def serialize(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'latest_value': self.latest_value,
            'open': self.open,
            'high':self.high,
            'low': self.latest_value,
            'close': self.close,
            'quote_date': self.quote_date,
            'effective_from': self.effective_from,
            'effective_to': self.effective_to
        }

    def __repr__(self):
        return self.name