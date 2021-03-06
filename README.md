# Currencies_Flask
В данной работе было реализованно HTPP API, с помощью которого можно получать данные об изменении курса валют,
а также список валют, о которых есть информация.
В данном проекте были использованы:
1. Flask т.к он наиболее подходит для создания небольших сервисов.
2. Стандартный модуль datetime, позволяющий быстро и удобно обрабатывать время и даты.
3. Модуль requests, с помощью которого происходит взаимодействие с cbr.ru по средствам HTTP запросов.
4. Модуль xml был использован для чтения ответов в формате XML, а также быстрого поиска необходимых данных
5. GitHub - система контроля версий, которая позволяет хранить и передавать код.
6. VirtualEnv для создания виртуального окружения, чтобы избежать конфликтов библиотек.
7. Postman использовался для проверки корректности ответов сервера и просмотра json-ответов.
8. SQLAlchemy для создания БД, в которой хранятся значения, которые уже были ранее запрощенны от сервера банка, чтобы снизить зависимость от него

Примеры вызова методов.

А)Вызов метода, передающего информацию о списке доступных валют:
http://127.0.0.1:5000/list_of_currencies

Пример ответа:

{
    "AMD": "Армянский драм",
    "AON": "Ангольская новая кванза",
    "ATS": "Австрийский шиллинг",
    "AUD": "Австралийский доллар",
    "AZN": "Азербайджанский манат",
    "BEF": "Бельгийский франк",
    "BGN": "Болгарский лев",
    "BRL": "Бразильский реал",
    "BYN": "Белорусский рубль",
    "CAD": "Канадский доллар",
    "CHF": "Швейцарский франк",
    "CNY": "Китайский юань",
    "CZK": "Чешская крона",
    "DEM": "Немецкая марка",
    "DKK": "Датская крона",
    "EEK": "Эстонская крона",
    "ESP": "Испанская песета",
    "EUR": "Евро",
    "FIM": "Финляндская марка",
    "FRF": "Французский франк",
    "GBP": "Фунт стерлингов Соединенного королевства",
    "GRD": "Греческая драхма",
    "HKD": "Гонконгский доллар",
    "HUF": "Венгерский форинт",
    "IEP": "Ирландский фунт",
    "INR": "Индийская рупия",
    "ISK": "Исландская крона",
    "ITL": "Итальянская лира",
    "JPY": "Японская иена",
    "KGS": "Киргизский сом",
    "KRW": "Вон Республики Корея",
    "KWD": "Кувейтский динар",
    "KZT": "Казахстанский тенге",
    "LBP": "Ливанский фунт",
    "LTL": "Литовский лит",
    "LVL": "Латвийский лат",
    "MDL": "Молдавский лей",
    "NLG": "Нидерландский гульден",
    "NOK": "Норвежская крона",
    "PLN": "Польский злотый",
    "PTE": "Португальский эскудо",
    "ROL": "Румынский лей",
    "RON": "Румынский лей",
    "SEK": "Шведская крона",
    "SGD": "Сингапурский доллар",
    "SRD": "Суринамский доллар",
    "TJR": "Таджикский рубл",
    "TJS": "Таджикский сомони",
    "TMM": "Туркменский манат",
    "TMT": "Новый туркменский манат",
    "TRY": "Турецкая лира",
    "UAH": "Украинская гривна",
    "USD": "Доллар США",
    "UZS": "Узбекский сум",
    "XDR": "СДР (специальные права заимствования)",
    "XEU": "ЭКЮ",
    "YUN": "Югославский новый динар",
    "ZAR": "Южноафриканский рэнд",
    "null": "Украинский карбованец"
}

Б)Вызов метода, который возвращает данные о курсе валюты за две даты, а также разницу в курсе валюты между первой и второй датой:
http://127.0.0.1:5000/changes_by_dates?date_from=2007-10-03&date_to=2015-10-04&currency=USD

date_from - первая дата

date_to - вторая дата

currency - символьный код валюты

Пример ответа:

{
    "Currency_value_from": 24.9093,
    "Currency_value_to": 65.9414,
    "Difference": -41.0321
}

