from flask import Flask, request, jsonify, make_response
import datetime
import requests
import os.path
import xml.etree.ElementTree as ET
from model import db, CurrenciesData


app = Flask(__name__)


# Configurate
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '3e4ftyg'
ALLOWED_EXTENSIONS = {'txt'}
db.init_app(app)


# Constants
URL_FOR_LIST = 'http://www.cbr.ru/scripts/XML_valFull.asp'
URL = 'http://www.cbr.ru/scripts/XML_daily.asp'

# Checks for the presence of a database, creates if necessary
def create_db():
    if os.path.exists('database.db'):
        print('DB already created')
    else:
        print('DB create')
        db.create_all(app=app)


# Checks if there is a record about the current day in the database, adds if necessary.
# Returns the value of the required currency
def save_in_db(date, currency):
    date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
    if bool(CurrenciesData.query.filter_by(date=date).first()):
        info = CurrenciesData.query.filter_by(date=date).one()
        tree = ET.fromstring(info.data_xml)
        for child in tree:
            if child.find('CharCode').text == currency:
                return float(child.find('Value').text.replace(',', '.'))
    else:
        try:
            response = requests.get(URL, params={'date_req': date})
            add = CurrenciesData(date=date, data_xml=response.text)
            db.session.add(add)
            db.session.commit()
        except Exception:
            return make_response('Incorrect data', 400)
        tree = ET.fromstring(response.text)
        for child in tree:
            if child.find('CharCode').text == currency:
                return float(child.find('Value').text.replace(',', '.'))


# Method that returns a list of currencies
@app.route("/list_of_currencies", methods=['get'])
def list_of_currencies():
    if os.path.exists('Currencies_list.txt'):
        file = open('Currencies_list.txt', 'r')
        tree = ET.fromstring(file.read())
        ans = {}
        for child in tree:
            ans[child.find('ISO_Char_Code').text] = child.find('Name').text
        return jsonify(ans)
    else:
        response = requests.get(URL_FOR_LIST)
        tree = ET.fromstring(response.text)
        ans = {}
        for child in tree:
            ans[child.find('ISO_Char_Code').text] = child.find('Name').text
        file = open('Currencies_list.txt', 'w+')
        file.write(response.text)
        file.close()
        return jsonify(ans)


# Method that returns the difference in the exchange rate by date
@app.route("/changes_by_dates", methods=['get'])
def changes_by_dates():
    if (request.args.get('date_from') and request.args.get('date_to') and request.args.get('currency')) != None:
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        currency = request.args.get('currency')
        try:
            first_date = save_in_db(date_from, currency)
            second_date = save_in_db(date_to, currency)
        except ValueError:
            return make_response("Incorrect date format, should be YYYY-MM-DD", 400)
        diff = first_date - second_date
        ans = {'currency_value_from': first_date,
                'currency_value_to': second_date,
                'difference': diff}
        return jsonify(ans)
    return make_response('Incorrect data', 400)


if __name__ == "__main__":
    create_db()
    app.run(debug=False)
