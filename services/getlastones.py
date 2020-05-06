import os
import json
import requests
from datetime import datetime

DATA_DIR = "./data"
url = "https://api.tinkoff.ru/v1/currency_rates"


def get_last_ones():
    r = requests.get(url=url)
    js = json.loads(r.text)

    DebitCardsTransfers = []
    for x in js['payload']['rates']:
        if x['category'] == 'DebitCardsTransfers':
            DebitCardsTransfers.append(x)

    res = {}
    for el in DebitCardsTransfers:
        if el['fromCurrency']['name'] == 'USD' and el['toCurrency']['name'] == 'RUB':
            res['dol'] = {'prod': str(el['buy']), 'pokup': str(el['sell'])}
        elif el['fromCurrency']['name'] == 'EUR' and el['toCurrency']['name'] == 'RUB':
            res['evr'] = {'prod': str(el['buy']), 'pokup': str(el['sell'])}
        elif el['fromCurrency']['name'] == 'GBP' and el['toCurrency']['name'] == 'RUB':
            res['funt'] = {'prod': str(el['buy']), 'pokup': str(el['sell'])}

    return res


def getit(now_str):
    now = datetime.today()
    csv_name = os.path.join(DATA_DIR, "data_" + str(now.year) + "_" + str(now.month) + ".csv")
    resp = get_last_ones()
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)
    if not os.path.exists(csv_name):
        with open(csv_name, 'w') as initfile:
            initfile.write("date;pokup_dol;pokup_evr;pokup_funt;prod_dol;prod_evr;prod_funt\n")
    with open(csv_name, 'a') as wfile:
        wfile.write(now_str + ";" + resp['dol']['pokup'] + ";" + resp['evr']['pokup'] + ";" + resp['funt']['pokup'] + \
                    ";" + resp['dol']['prod'] + ";" + resp['evr']['prod'] + ";" + resp['funt']['prod'] + "\n")
