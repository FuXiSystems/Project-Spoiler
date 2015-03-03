__author__ = 'Mohamed'
from app.models.model import Model

from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Date, DateTime, Text


class Client(Model):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), unique=True, nullable=True)
    forename = Column(String(255), nullable=True)
    surname = Column(String(255), nullable=True)
    title = Column(String(255), nullable=True)
    shortname = Column(String(50), nullable=True)
    #    adviser_id = Column(db.Integer, db.ForeignKey('advisers.id'), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    ni_number = Column(String(10), nullable=True)
    image_id = Column(Integer, nullable=True)
    effective_from = Column(DateTime, nullable=True)
    effective_to = Column(DateTime, nullable=True)

    #    adviser = relationship("Advisers")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'forename': self.forename,
            'surname': self.surname,
            'title': self.title,
            'shortname': self.shortname,
            #'adviser_id': self.adviser_id,
            'date_of_birth': self.date_of_birth,
            'ni_number': self.ni_number,
            'image_id': self.image_id,
            'effective_from': self.effective_from,
            'effective_to': self.effective_to
        }


def __repr__(self):
    return self.name
