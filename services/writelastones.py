import os
from datetime import datetime
from services.getlastones import decorate_last_ones

DATA_DIR = "./data"


def write_last(now_str):
    now = datetime.today()
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)
    year_dir = os.path.join(DATA_DIR, str(now.year))
    if not os.path.isdir(year_dir):
        os.mkdir(year_dir)
    csv_name = os.path.join(year_dir, str(now.month) + ".csv")
    resp = decorate_last_ones()

    if resp:
        if not os.path.exists(csv_name):
            with open(csv_name, 'w') as initfile:
                initfile.write(
                    "date;pokup_dol;pokup_evr;pokup_funt;prod_dol;prod_evr;prod_funt;pokup_dol_n;pokup_evr_n;pokup_funt_n;prod_dol_n;prod_evr_n;prod_funt_n\n")
        with open(csv_name, 'a') as wfile:
            wfile.write(now_str[:now_str.index(".")] + ";" + resp['dol']['pokup'] + ";" + resp['evr']['pokup'] + ";" + \
                        resp['funt']['pokup'] + ";" + resp['dol']['prod'] + ";" + resp['evr']['prod'] + ";" + \
                        resp['funt']['prod'] + ";" + resp['dol']['pokup_n'] + ";" + resp['evr']['pokup_n'] + ";" + \
                        resp['funt']['pokup_n'] + ";" + resp['dol']['prod_n'] + ";" + resp['evr']['prod_n'] + ";" + \
                        resp['funt']['prod_n'] + "\n")
