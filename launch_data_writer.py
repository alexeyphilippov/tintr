import time
from datetime import datetime
from services.writelastones import write_last
from utils.logger import log

MAX_SECS = 60

while True:
    now = str(datetime.today())
    try:
        write_last(now_str=now)
    except Exception as e:
        log("Exception in launch_data_writer " + str(e))
        continue
    time.sleep(MAX_SECS)
