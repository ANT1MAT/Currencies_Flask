from flask import Flask, request, jsonify, abort, make_response
import datetime
import requests
import xml.etree.ElementTree as ET


app = Flask(__name__)


# Configurate
app.config['JSON_AS_ASCII'] = False


# Constants
URL_FOR_LIST = 'http://www.cbr.ru/scripts/XML_valFull.asp'
URL = 'http://www.cbr.ru/scripts/XML_daily.asp'


def find_currency_value(date, currency):
    response = requests.get(URL, params={'date_req': date})
    tree = ET.fromstring(response.text)
    for child in tree:
        if child.find('CharCode').text == currency:
            return float(child.find('Value').text.replace(',', '.'))
    return 'Not Data'


@app.route("/list_of_currencies", methods=['get'])
def list_of_currencies():
    response = requests.get(URL_FOR_LIST)
    tree = ET.fromstring(response.text)
    ans = {}
    for child in tree:
        ans[child.find('ISO_Char_Code').text] = child.find('Name').text
    return jsonify(ans)


@app.route("/changes_by_dates", methods=['get'])
def changes_by_dates():
    if (request.args.get('date_from') and request.args.get('date_to') and request.args.get('currency')) != None:
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        try:
            datetime.datetime.strptime(date_from, '%Y-%m-%d')
            datetime.datetime.strptime(date_to, '%Y-%m-%d')
        except ValueError:
            return make_response("Incorrect date format, should be YYYY-MM-DD", 400)
        currency = request.args.get('currency')
        date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d").strftime("%d/%m/%Y")
        date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d").strftime("%d/%m/%Y")
        try:
            diff = find_currency_value(date_from, currency) - find_currency_value(date_to, currency)
            ans = {'currency_value_from': find_currency_value(date_from, currency),
                    'currency_value_to': find_currency_value(date_to, currency),
                    'difference': diff}
        except:
            ans = {'currency_value_from': find_currency_value(date_from, currency),
                   'currency_value_to': find_currency_value(date_to, currency),
                   'difference': 'Can\'t calculated'}
        return jsonify(ans)
    else:
        return make_response('Incorrect data', 400)


if __name__ == "__main__":
    app.run(debug=False)
