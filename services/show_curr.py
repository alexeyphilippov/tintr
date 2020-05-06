import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime 
import datetime as dt

import warnings
warnings.filterwarnings("ignore")

def show(trigger:float=None,currency:str='EUR', both_bounds:bool=False, presiceness:str='hour'):
    """
        currency : ['USD', 'EUR', 'GBP']
        both_bounds : wheather or not to show both buy and sell
        presiceness : ['hour', '6hours', 'day', 'month'] #TODO
    """
    
    spreads = {'dol': 0.01,
          'evr':0.01,
          'funt':0.016}
    
    delta, min_int = dt.timedelta(hours=1), 5
    if presiceness=='6hours' : delta, min_int = dt.timedelta(hours=6), 30
    elif presiceness=='day': delta, min_int  = dt.timedelta(days=1), 80
    elif presiceness=='month': delta, min_int  = dt.timedelta(days=31), 360
    elif presiceness=='hour':pass
    else: print("Invalid presiceness set default to 1 hour")

    striptime = lambda x: datetime.strptime(x,"%Y-%m-%d %H:%M:%S")
    data = pd.read_csv("data/data_2020_"+str(datetime.now().month)+".csv", sep=';')
    data.date = data.date.apply(lambda x: x[:x.index('.')]).apply(striptime)    
    data2 = data[data.date > datetime.now() - delta]
    data2['mean_funt'] = (data2.pokup_funt + data2.prod_funt)/2
    data2['mean_evr'] = (data2.pokup_evr + data2.prod_evr)/2
    data2['mean_dol'] = (data2.pokup_dol + data2.prod_dol)/2
    data_night = data2[data2.mean_evr > 0.03]
    data_night['prod_dol_n'] = data_night['mean_dol'] - data_night['mean_dol'] * spreads['dol']/2
    data_night['prod_evr_n'] = data_night['mean_evr'] - data_night['mean_evr'] * spreads['evr']/2
    data_night['prod_funt_n'] = data_night['mean_funt'] - data_night['mean_funt'] * spreads['funt']/2

    data_night['pokup_dol_n'] = data_night['mean_dol'] + data_night['mean_dol'] * spreads['dol']/2
    data_night['pokup_evr_n'] = data_night['mean_evr'] + data_night['mean_evr'] * spreads['evr']/2
    data_night['pokup_funt_n'] = data_night['mean_funt'] + data_night['mean_funt'] * spreads['funt']/2

    dates = data2.date.tolist()
    dates_night = data_night.date.tolist()
    x = dates
    x_n = dates_night
    y1 = data2.prod_evr.tolist()
    y3 = data2.pokup_evr.tolist()
    y1_n = data_night.prod_evr_n.tolist()
    y3_n = data_night.pokup_evr_n.tolist()
    if currency=='USD':
        y1 = data2.prod_dol.tolist()
        y3 = data2.pokup_dol.tolist()
        y1_n = data_night.prod_dol_n.tolist()
        y3_n = data_night.pokup_dol_n.tolist()
    elif currency=='GBP':
        y1 = data2.prod_funt.tolist()
        y3 = data2.pokup_funt.tolist()
        y1_n = data_night.prod_funt_n.tolist()
        y3_n = data_night.pokup_funt_n.tolist()
    elif currency=='EUR':
        pass
    else:
        print("Invalid currency set default to EUR")
    if trigger: y2 = [trigger] * len(y1)

    fig = plt.figure(figsize=(7.5,5))
    if presiceness=='month':
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xlim(left=x[0],right=x[-1] + dt.timedelta(days=2))
    elif presiceness=='hour':
        plt.xlim(left=x[0],right=x[-1] + dt.timedelta(minutes=10))
    elif presiceness=='day':
        plt.xlim(left=x[0],right=x[-1] + dt.timedelta(hours=2))
    elif presiceness=='6hours':
        plt.xlim(left=x[0],right=x[-1] + dt.timedelta(hours=1))
    else:
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.xlim(right=datetime.now() + dt.timedelta(hours=1))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=min_int))
    if trigger:
        if both_bounds:
            res =  plt.plot(x, y1, 'k', x, y2, 'r-', x, y3, 'b', x_n, y1_n, 'k--', x_n, y3_n, 'b--')
            plt.legend(handles=res, labels=('Я продаю','Мой траггер','Я покупаю'))
            plt.annotate(str(y3[-1]), xy=(x[-1], y3[-1]))
        else:
            res =  plt.plot(x, y1, 'k', x, y2, 'r-', x_n, y1_n, 'k--')
            plt.legend(handles=res, labels=('Я продаю','Мой траггер'))
    else:
        if both_bounds:
            res =  plt.plot(x, y1, 'k', x, y3, 'b', x_n, y1_n, 'k--', x_n, y3_n, 'b--')
            plt.legend(handles=res, labels=('Я продаю','Я покупаю'))
            plt.annotate(str(y3[-1]), xy=(x[-1], y3[-1]))
        else:
            res =  plt.plot(x, y1, 'k', x_n, y1_n, 'k--')
            plt.legend(handles=res, labels=(('Продаю',)))
    plt.gcf().autofmt_xdate()
    plt.grid()
    plt.annotate(str(y1[-1]), xy=(x[-1], y1[-1]))
    _ = plt.title(pad=10, label='Курс {} за последние {}'.format(currency, presiceness))
    