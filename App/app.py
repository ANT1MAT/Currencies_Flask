from flask import Flask, request, jsonify, abort
import datetime
import requests
import xml.etree.ElementTree as ET


app = Flask(__name__)


#Configurate
app.config['JSON_AS_ASCII'] = False


#Constants
url_for_list = 'http://www.cbr.ru/scripts/XML_valFull.asp'
url = 'http://www.cbr.ru/scripts/XML_daily.asp'


def find_currency_value(date, currency):
    response = requests.get(url, params={'date_req': date})
    tree = ET.fromstring(response.text)
    print(date)
    for child in tree:
        print(child.find('CharCode').text)
        if child.find('CharCode').text == currency:
            return float(child.find('Value').text.replace(',', '.'))
    return 'Not Data'


def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        return abort(412)


@app.route("/list_of_currencies", methods=['get'])
def list_of_currencies():
        response = requests.get(url_for_list)
        tree = ET.fromstring(response.text)
        ans = {}
        for child in tree:
            ans[child.find('ISO_Char_Code').text] = child.find('Name').text
        return jsonify(ans)


@app.route("/changes_by_dates", methods=['get'])
def changes_by_dates():
    if request.args.get('date_from') and request.args.get('date_to') and request.args.get('currency') != None:
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        validate_date(date_from)
        validate_date(date_to)
        currency = request.args.get('currency')
        date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d").strftime("%d/%m/%Y")
        date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d").strftime("%d/%m/%Y")
        try:
            diff = find_currency_value(date_from, currency) - find_currency_value(date_to, currency)
            ans = {'Currency_value_from': find_currency_value(date_from, currency),
                    'Currency_value_to': find_currency_value(date_to, currency),
                    'Difference': diff}
        except:
            ans = {'Currency_value_from': find_currency_value(date_from, currency),
                   'Currency_value_to': find_currency_value(date_to, currency),
                   'Difference': 'Can\'t calculated'}
        return jsonify(ans)
    else:
        return ValueError('Data not transmitted')


if __name__ == "__main__":
    app.run(debug=True)
