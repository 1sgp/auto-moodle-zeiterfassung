# moodle-auto-Zeiterfassung
# v0.4.0
# 2023-09-28
# contribute @ github.com/1sgp/moodle-zeiterfassung

from datetime import datetime as dt
from datetime import time as t
from datetime import timedelta as td
from random import randint
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time
from dates import days
from browser import init as init
from browser import login_user, login_check, handleAlert, handleDatapref, wait
from browser import link as link
from utils import clear, enter_creds, Times
from wrap import main as Zeiterfassung

us0r = ""
w0rd = ""
days = days

def main():
    clear()
    print("Hello World.")
    print(dt.now().isoformat())
    while True:
        dates = [day for day in days if day >= dt.now().date().strftime("%Y/%m/%d")]
        if dt.now().date().strftime("%Y/%m/%d") in dates:
            pass
        else:
            delta = round((dt.strptime(dates[0], "%Y/%m/%d") + td(hours=8) - dt.now()).total_seconds())
            sleep(delta)
            continue
        
        while True:
            if dt.now().time() < t(16, 40):
                selection = True if input("Home = 1, Standort = 2: ") == "1" else False
                status = Zeiterfassung(us0r, w0rd, selection)
            else:
                if dt.now().date().strftime("%Y/%m/%d") in dates:
                    days.pop(0)
                break
