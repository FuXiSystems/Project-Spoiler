__author__ = 'Mohamed'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool

import config


def get_db():

    engine = get_engine()

    db_session = scoped_session(sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    ))

    return db_session


def get_engine():
    engine = create_engine(
                config.DATABASE_URI.format(
                    username=config.USERNAME,
                    password=config.PASSWORD,
                    database=config.USERNAME,
                    host=config.HOST,
                    port=int(config.DB_PORT)
                )
    )

    return engine

# Returns all non-nullable fields per object as set - we do set operations anyway so might as well roll with that
# Probably worth ingraining this into model inheritance but will leave this here for now
def get_required_fields(instance):
    columns = instance.__table__.columns
    required_fields = set()
    for column in columns:
        if not column.nullable and not column.primary_key:
            required_fields.add(column.name)

    return required_fields