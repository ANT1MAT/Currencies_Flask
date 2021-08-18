from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CurrenciesData(db.Model):
    __tablename__ = 'Currencies Data'
    date = db.Column(db.Text, primary_key=True)
    data_xml = db.Column(db.Text)