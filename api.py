
import datetime
import logging

import flask

from flask import Flask, url_for
from flask import request
from flask import Response
from flask import json
from flask import jsonify

from functools import wraps

from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

import flask_sqlalchemy
import flask.ext.restless

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKey, Index, Integer, Numeric, String, Table, Text, text
#from sqlalchemy import create_engine

from sqlalchemy.orm import backref, relationship
#from sqlalchemy.orm import scoped_session, sessionmaker


#from sqlalchemy.ext.declarative import declarative_base

# Create the Flask application.
app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://fuxiadmin:admin123@fuxi.cjbrs9qrutbu.us-west-2.rds.amazonaws.com:5432/wms'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:casper@localhost/wms'

# Create the db Connection
db = flask.ext.sqlalchemy.SQLAlchemy(app)


# Setup the application logging.
file_handler = logging.FileHandler('api.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

def today():
    return datetime.datetime.today().strftime('\%Y-\%m-\%d')

##############################################################################
#
#	Some Athentication and Logging functions to build on
#
#
#
#




def check_auth(username, password):
    return username == 'admin' and password == 'secret'

def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'
    resp.headers.add('WWW-Authenticate', 'Bearer realm="Example"')

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth: 
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated

@app.route('/secrets')
@requires_auth
def api_hello3():
    return "Shhh this is top secret spy stuff!"


@app.route('/hello4', methods = ['GET'])
def api_hello4():
    app.logger.info('informing')
    app.logger.warning('warning')
    app.logger.error('screaming bloody murder!')
    
    return "check your logs\n"

#
#
#
#
#
#
##############################################################################

##############################################################################
#
#	Some General Error handling to ensure a JSON response is always sent
#
#
#
#

__all__ = ['make_json_app']

def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """
    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app

#
#
#
#
#
##############################################################################


# Define all the db models

class Globals(db.Model):
    __tablename__ = 'globals'

    id = Column(Integer, primary_key=True , nullable=False) 
    code = Column(String(8000), nullable=True) 
    value = Column(String(8000), nullable=True) 
    datatype = Column(String(8000), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


class Lookups(db.Model):
    __tablename__ = 'lookups'

    id = Column(Integer, primary_key=True , nullable=False) 
    type = Column(String(255), nullable=True) 
    code = Column(String(255), nullable=True) 
    basetype = Column(String(255), nullable=True) 
    table_name = Column(String(255), nullable=True) 
    table_key = Column(String(255), nullable=True) 
    value = Column(String(255), nullable=True) 
    shortname = Column(String(255), nullable=True) 
    name = Column(String(255), nullable=True) 
    title = Column(String(255), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


    def __repr__(self):
        return self.name

class LookupCodes(db.Model):
    __tablename__ = 'lookup_codes'

    id = Column(Integer, primary_key=True , nullable=False) 
    type = Column(String(255), nullable=False) 
    code = Column(String(255), nullable=False) 
    value = Column(String(255), nullable=False) 
    name = Column(String(255), nullable=True) 
    shortname = Column(String(30), nullable=True) 
    sequence = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


    def __repr__(self):
        return self.name

class Logs(db.Model):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True , nullable=False) 
    message = Column(String(16384), nullable=True) 
    message_source = Column(String(255), nullable=True) 
    message_depth = Column(Integer, nullable=True) 
    message_severity = Column(String(30), nullable=True) 
    message_date = Column(DateTime, nullable=True) 
    message_user = Column(String(100), nullable=True) 
    logs_date = Column(DateTime, nullable=True) 
    user_id = Column(String(100), nullable=True) 


class QueryDetailColumns(db.Model):
    __tablename__ = 'query_detail_columns'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), nullable=True) 
    column_sequence = Column(Integer, nullable=True) 
    column_name = Column(String(50), nullable=True) 
    column_title = Column(String(50), nullable=True) 
    column_summary = Column(String(50), nullable=True) 
    column_precedence = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


    def __repr__(self):
        return self.name

class Objects(db.Model):
    __tablename__ = 'objects'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), nullable=True) 
    id_name = Column(String(255), nullable=True) 
    value_name = Column(String(255), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


    def __repr__(self):
        return self.name

class CrossReferences(db.Model):
    __tablename__ = 'cross_references'

    id = Column(Integer, primary_key=True , nullable=False) 
    object_type = Column(String(255), nullable=True) 
    object_id = Column(Integer, nullable=True) 
    xref_type = Column(String(255), nullable=True) 
    xref_value = Column(String(255), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


class ClientContacts(db.Model):
    __tablename__ = 'client_contacts'

    id = Column(Integer, primary_key=True , nullable=False) 
    client_id = Column(Integer, nullable=True) 
    contact_id = Column(Integer, nullable=True) 
    sequence = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


class Columns(db.Model):
    __tablename__ = 'columns'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(8000), unique=True , nullable=True) 
    title = Column(String(8000), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


    def __repr__(self):
        return self.name

class UserColumns(db.Model):
    __tablename__ = 'user_columns'

    id = Column(Integer, primary_key=True , nullable=False) 
    user_id = Column(Integer, nullable=True) 
    object_name = Column(String(8000), nullable=True) 
    column_name = Column(String(8000), nullable=True) 
    column_title = Column(String(8000), nullable=True) 
    column_order = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


class Feed(db.Model):
    __tablename__ = 'feed'

    id = Column(Integer, primary_key=True , nullable=False) 
    feed_id = Column(Integer, nullable=True) 
    feed_type = Column(String(255), nullable=True) 
    source_system = Column(String(255), nullable=True) 
    source_reference = Column(String(8000), nullable=True) 
    tag = Column(String(8000), nullable=True) 
    value = Column(String(8000), nullable=True) 
    value_sequence = Column(Integer, nullable=True) 
    state = Column(Integer, nullable=True) 
    target_state = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


class Data(db.Model):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True , nullable=False) 
    data_id = Column(Integer, nullable=True) 
    data_type = Column(String(255), nullable=True) 
    source_system = Column(String(255), nullable=True) 
    source_reference = Column(String(8000), nullable=True) 
    tag = Column(String(8000), nullable=True) 
    value = Column(String(8000), nullable=True) 
    value_sequence = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


class PreferencePriorities(db.Model):
    __tablename__ = 'preference_priorities'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), nullable=True) 
    priority = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


    def __repr__(self):
        return self.name

class IndexComponents(db.Model):
    __tablename__ = 'index_components'

    id = Column(Integer, primary_key=True , nullable=False) 
    index_id = Column(Integer, ForeignKey('indices.id'), nullable=True) 
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True) 
    sequence = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 

    product = relationship("Products") 
    index = relationship("Indices") 

class ContactSocialNetworks(db.Model):
    __tablename__ = 'contact_social_networks'

    id = Column(Integer, primary_key=True , nullable=False) 
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=True) 
    social_network_id = Column(Integer, ForeignKey('social_networks.id'), nullable=True) 
    identifier = Column(String(255), unique=True , nullable=True) 
    sequence = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 

    social_network = relationship("SocialNetworks") 
    contact = relationship("Contacts") 

class UserRoles(db.Model):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True , nullable=False) 
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True) 
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 

    role = relationship("Roles") 
    user = relationship("Users") 

class HistoricQuotes(db.Model):
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

class PortfolioPositions(db.Model):
    __tablename__ = 'portfolio_positions'

    id = Column(Integer, primary_key=True , nullable=False) 
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=True) 
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True) 
    currency = Column(String(3), nullable=True) 
    quantity = Column(Integer, nullable=True) 
    price = Column(Numeric(36,8), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 

    product = relationship("Products") 
    portfolio = relationship("Portfolios") 

class RoleRights(db.Model):
    __tablename__ = 'role_rights'

    id = Column(Integer, primary_key=True , nullable=False) 
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True) 
    object_type = Column(String(255), nullable=True) 
    object_name = Column(String(255), nullable=True) 
    object_subname = Column(String(255), nullable=True) 
    access_rights = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 

    role = relationship("Roles") 

class HistoricPrices(db.Model):
    __tablename__ = 'historic_prices'

    id = Column(Integer, primary_key=True , nullable=False) 
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True) 
    price_date = Column(DateTime, nullable=True) 
    open = Column(Numeric(36,8), nullable=True) 
    high = Column(Numeric(36,8), nullable=True) 
    low = Column(Numeric(36,8), nullable=True) 
    close = Column(Numeric(36,8), nullable=True) 
    volume = Column(Numeric(36,8), nullable=True) 
    adj_close = Column(Numeric(36,8), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 

    product = relationship("Products") 

class DiaryEntries(db.Model):
    __tablename__ = 'diary_entries'

    id = Column(Integer, primary_key=True , nullable=False) 
    diary_id = Column(Integer, ForeignKey('diaries.id'), nullable=True) 
    subject = Column(String(255), nullable=True) 
    location = Column(String(255), nullable=True) 
    start_time = Column(DateTime, nullable=True) 
    end_time = Column(DateTime, nullable=True) 
    details = Column(Text, nullable=True) 
    notes = Column(Text, nullable=True) 
    user_id = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=True) 

    client = relationship("Clients") 
    diary = relationship("Diaries") 

class Logins(db.Model):
    __tablename__ = 'logins'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), nullable=False) 
    title = Column(String(255), nullable=False) 
    username = Column(String(255), nullable=False) 
    password = Column(String(255), nullable=False) 
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True) 
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True) 
    last_login = Column(DateTime, nullable=True) 
    one_off = Column(DateTime, nullable=True) 
    is_suspended = Column(String(1), nullable=False) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 

    user = relationship("Users") 
    role = relationship("Roles") 

    def __repr__(self):
        return self.name

class Quotes(db.Model):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True , nullable=False) 
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True) 
    latest_value = Column(Numeric(36,8), nullable=True) 
    open = Column(Numeric(36,8), nullable=True) 
    high = Column(Numeric(36,8), nullable=True) 
    low = Column(Numeric(36,8), nullable=True) 
    mid = Column(Numeric(36,8), nullable=True) 
    close = Column(Numeric(36,8), nullable=True) 
    bid = Column(Numeric(36,8), nullable=True) 
    offer = Column(Numeric(36,8), nullable=True) 
    quote_date = Column(DateTime, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 

    product = relationship("Products") 

class Products(db.Model):
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

    def __repr__(self):
        return self.name

class Contacts(db.Model):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), unique=True , nullable=True) 
    title = Column(String(255), nullable=True) 
    position = Column(String(255), nullable=True) 
    forename = Column(String(255), nullable=True) 
    surname = Column(String(255), nullable=True) 
    honours = Column(String(255), nullable=True) 
    phone = Column(String(255), nullable=True) 
    email = Column(String(255), nullable=True) 
    address_name = Column(String(255), nullable=True) 
    address_no = Column(String(255), nullable=True) 
    address_street = Column(String(255), nullable=True) 
    address_district = Column(String(255), nullable=True) 
    address_town = Column(String(255), nullable=True) 
    address_city = Column(String(255), nullable=True) 
    address_county = Column(String(255), nullable=True) 
    address_country = Column(String(255), nullable=True) 
    address_postcode = Column(String(255), nullable=True) 
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=True) 
    sequence = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 

    client = relationship("Clients") 

    def __repr__(self):
        return self.name

class Diaries(db.Model):
    __tablename__ = 'diaries'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), unique=True , nullable=True) 
    title = Column(String(255), nullable=True) 
    nickname = Column(String(50), nullable=True) 
    adviser_id = Column(Integer, ForeignKey('advisers.id'), nullable=True) 
    user_id = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 

    adviser = relationship("Advisers") 

    def __repr__(self):
        return self.name

class SocialNetworks(db.Model):
    __tablename__ = 'social_networks'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), unique=True , nullable=True) 
    title = Column(String(255), nullable=True) 
    nickname = Column(String(50), nullable=True) 
    website = Column(String(255), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


    def __repr__(self):
        return self.name

class Roles(db.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True , nullable=False) 
    role = Column(String(50), nullable=False) 
    name = Column(String(255), nullable=False) 
    title = Column(String(255), nullable=False) 
    shortname = Column(String(50), nullable=False) 
    precedence = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


    def __repr__(self):
        return self.name

class Indices(db.Model):
    __tablename__ = 'indices'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), unique=True , nullable=True) 
    title = Column(String(255), nullable=True) 
    nickname = Column(String(50), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


    def __repr__(self):
        return self.name

class Portfolios(db.Model):
    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(50), unique=True , nullable=True) 
    title = Column(String(50), nullable=True) 
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=True) 
    nickname = Column(String(50), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 

    client = relationship("Clients") 

    def __repr__(self):
        return self.name

class Clients(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True , nullable=False) 
    name = db.Column(db.String(255), unique=True , nullable=True) 
    forename = db.Column(db.String(255), nullable=True) 
    surname = db.Column(db.String(255), nullable=True) 
    title = db.Column(db.String(255), nullable=True) 
    shortname = db.Column(db.String(50), nullable=True) 
#    adviser_id = db.Column(db.Integer, db.ForeignKey('advisers.id'), nullable=True) 
    date_of_birth = db.Column(db.Date, nullable=True) 
    ni_number = db.Column(db.String(10), nullable=True) 
    image_id = db.Column(db.Integer, nullable=True) 
    effective_from = db.Column(db.DateTime, nullable=True) 
    effective_to = db.Column(db.DateTime, nullable=True) 

#    adviser = relationship("Advisers") 

    def __repr__(self):
        return self.name

class Instruments(db.Model):
    __tablename__ = 'instruments'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), unique=True , nullable=True) 
    title = Column(String(255), nullable=True) 
    nickname = Column(String(50), nullable=True) 
    symbol = Column(String(50), nullable=True) 
    currency = Column(String(3), nullable=True) 
    instrument_type_id = Column(Integer, ForeignKey('instrument_types.id'), nullable=True) 
    instrument_category_id = Column(Integer, ForeignKey('instrument_categories.id'), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 

    instrument_category = relationship("InstrumentCategories") 
    instrument_type = relationship("InstrumentTypes") 

    def __repr__(self):
        return self.name

class Exchanges(db.Model):
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

    def __repr__(self):
        return self.name

class Countries(db.Model):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), unique=True , nullable=True) 
    title = Column(String(255), nullable=True) 
    nickname = Column(String(50), nullable=True) 
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 

    currency = relationship("Currencies") 

    def __repr__(self):
        return self.name

class Advisers(db.Model):
    __tablename__ = 'advisers'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), unique=True , nullable=True) 
    title = Column(String(255), nullable=True) 
    nickname = Column(String(50), nullable=True) 
    forenames = Column(String(255), nullable=True) 
    surname = Column(String(255), nullable=True) 
    phone = Column(String(255), nullable=True) 
    email = Column(String(255), nullable=True) 
    managed_by_id = Column(Integer, ForeignKey('advisers.id'), nullable=True) 
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 

    user = relationship("Users") 
    manages = relationship("Advisers") 

    def __repr__(self):
        return self.name

class InstrumentTypes(db.Model):
    __tablename__ = 'instrument_types'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), unique=True , nullable=True) 
    title = Column(String(255), nullable=True) 
    nickname = Column(String(50), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


    def __repr__(self):
        return self.name

class InstrumentCategories(db.Model):
    __tablename__ = 'instrument_categories'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), unique=True , nullable=True) 
    title = Column(String(255), nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


    def __repr__(self):
        return self.name

class Currencies(db.Model):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), unique=True , nullable=True) 
    title = Column(String(255), nullable=True) 
    nickname = Column(String(50), nullable=True) 
    minor_unit = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


    def __repr__(self):
        return self.name

class Users(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True , nullable=False) 
    name = Column(String(255), nullable=True) 
    title = Column(String(255), nullable=True) 
    shortname = Column(String(50), nullable=True) 
    user_type = Column(String(50), nullable=True) 
    type_id = Column(Integer, nullable=True) 
    badge_number = Column(Integer, nullable=True) 
    is_suspended = Column(Integer, nullable=True) 
    effective_from = Column(DateTime, nullable=True) 
    effective_to = Column(DateTime, nullable=True) 


    def __repr__(self):
        return self.name


# Create your Flask-SQLALchemy models as usual but with the following two
# (reasonable) restrictions:
#   1. They must have a primary key column of type sqlalchemy.Integer or
#      type sqlalchemy.Unicode.
#   2. They must have an __init__ method which accepts keyword arguments for
#      all columns (the constructor in flask.ext.sqlalchemy.SQLAlchemy.Model
#      supplies such a method, so you don't need to declare a new one).
#class Person(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.Unicode, unique=True)
#    birth_date = db.Column(db.Date)
#
#class Computer(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.Unicode, unique=True)
#    vendor = db.Column(db.Unicode)
#    purchase_time = db.Column(db.DateTime)
#    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
#    owner = db.relationship('Person', backref=db.backref('computers',
#                                                         lazy='dynamic'))
#

# Create the database tables.
# db.create_all()

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.

#manager.create_api(Clients, methods=['GET', 'POST', 'DELETE'], include_columns = [ 'id' ,  'name' ,  'forename' ,  'surname' ,  'title' ,  'shortname' ,  'date_of_birth' ,  'ni_number' ,  'image_id' ,  'effective_from' ,  'effective_to' ] )

manager.create_api(Globals, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Lookups, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(LookupCodes, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Logs, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(QueryDetailColumns, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Objects, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(CrossReferences, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(ClientContacts, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Columns, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(UserColumns, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Feed, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Data, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(PreferencePriorities, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(IndexComponents, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(ContactSocialNetworks, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(UserRoles, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(HistoricQuotes, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(PortfolioPositions, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(RoleRights, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(HistoricPrices, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(DiaryEntries, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Logins, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Quotes, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Products, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Contacts, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Diaries, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(SocialNetworks, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Roles, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Indices, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Portfolios, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Clients, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Instruments, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Exchanges, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Countries, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Advisers, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(InstrumentTypes, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(InstrumentCategories, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Currencies, methods=['GET', 'POST', 'DELETE'] )
manager.create_api(Users, methods=['GET', 'POST', 'DELETE'] )


# start the flask loop
app.run()



