__author__ = 'Mohamed'
from sqlalchemy.ext.declarative import declarative_base

from app.services.database import get_engine

engine = get_engine()
Model = declarative_base(bind=engine)
