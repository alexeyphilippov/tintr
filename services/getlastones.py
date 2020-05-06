import json
import requests

from utils.logger import log

url = "https://api.tinkoff.ru/v1/currency_rates"


def get_last_ones():
    r = requests.get(url=url)
    js = json.loads(r.text)

    DebitCardsTransfers = []
    for x in js['payload']['rates']:
        if x['category'] == 'DebitCardsTransfers':
            DebitCardsTransfers.append(x)

    res = {}
    try:
        for el in DebitCardsTransfers:
            if el['fromCurrency']['name'] == 'USD' and el['toCurrency']['name'] == 'RUB':
                res['dol'] = {'prod': str(el['buy']), 'pokup': str(el['sell'])}
            elif el['fromCurrency']['name'] == 'EUR' and el['toCurrency']['name'] == 'RUB':
                res['evr'] = {'prod': str(el['buy']), 'pokup': str(el['sell'])}
            elif el['fromCurrency']['name'] == 'GBP' and el['toCurrency']['name'] == 'RUB':
                res['funt'] = {'prod': str(el['buy']), 'pokup': str(el['sell'])}
    except Exception as e:
        log("Error in get_last_ones" + str(e))
        return None
    return res


def decorate_last_ones():
    currencies = ['dol', 'evr', 'funt']
    spreads = {'dol': 0.01,
               'evr': 0.01,
               'funt': 0.016}
    r = get_last_ones()
    if r:
        mean_dol = (float(r['dol']['pokup']) + float(r['dol']['prod'])) / 2
        dif_dol = (float(r['dol']['pokup']) - float(r['dol']['prod']))
        spread_dol = dif_dol / mean_dol
        is_night = spread_dol > 0.03
        for curr in currencies:
            mean = (float(r[curr]['pokup']) + float(r[curr]['prod'])) / 2 if is_night else None
            r[curr]['prod_n'] = str(round(mean - (mean * spreads[curr] / 2), 2)) if is_night else None
            r[curr]['pokup_n'] = str(round(mean + (mean * spreads[curr] / 2), 2)) if is_night else None
        return r
    else:
        return None
