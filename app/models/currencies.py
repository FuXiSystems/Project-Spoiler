__author__ = 'Mohamed'

from app.models.model import Model

from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Date, DateTime, Text


class Currencies(Model):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True , nullable=False)
    name = Column(String(255), unique=True , nullable=True)
    title = Column(String(255), nullable=True)
    nickname = Column(String(50), nullable=True)
    minor_unit = Column(Integer, nullable=True)
    effective_from = Column(DateTime, nullable=True)
    effective_to = Column(DateTime, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'nickname': self.nickname,
            'minor_unit': self.minor_unit,
            'effective_from': self.effective_from,
            'effective_to': self.effective_to
        }


    def __repr__(self):
        return self.name
