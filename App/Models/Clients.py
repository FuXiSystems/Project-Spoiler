__author__ = 'Mohamed'
app = flask.Flask(__name__)
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://fuxiadmin:admin123@fuxi.cjbrs9qrutbu.us-west-2.rds.amazonaws.com:5432/wms'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5400/wms'

# Create the db Connection
db = flask.ext.sqlalchemy.SQLAlchemy(app)

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
