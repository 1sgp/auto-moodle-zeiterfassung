# autoZeiterfassung 0.3.2
# 2023-09-01

from datetime import datetime as dt
from datetime import timedelta as td
from random import randint
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep, time
from dates import ondays
from browser import init as init
from browser import getFullName, login_user, login_check, safeget
from browser import link as link
from utils import clear, countdown, enter_creds

browser = init()

class instance():
    @classmethod
    def __init__(self):
        now = dt.now()
        self.start_time = time()
        self.start_date = now.date()
    def countDays(self):
        td = dt.date() - self.start_date
        self.days_running = td.days

class ZE:
    reason = False
    running = False
    done = False
    startzeit = "NaN"
    endzeit = "NaN"
    startzeitstr = ""
    endzeitstr = ""
    now = dt.now()
    feierabend = dt(now.year, now.month, now.day, 16, 30)
    @classmethod
    def update(self, browser):
        status, started, stopped = ZE_get(browser)
        self.now = dt.now()
        self.running = status
        self.startzeitstr = started
        self.endzeitstr = stopped
        self.startzeit = dt.strptime(started, '%H:%M') if started[-1].isdigit() is True else "NaN"
        self.endzeit = dt.strptime(stopped, '%H:%M') if stopped[-1].isdigit() is True else "NaN"

class times:
    start_minmin = 10        #Minimum Minute for randominzing Start (8:<start_minmin> = 8:00) - Change here if needed - ex.: set to 15 for a random login time between 8:15 and 8:30. (default 0)
    start_maxmin = 26       #Minimum Minute for randominzing Start (8:<start_maxmin> = 8:30) - Change here if needed - ex.: set to 15 for a random login time between 8:00 and 8:15. (default 29)
    end_minmin = 31         #Minimum Minute for randominzing Feierabend (16:<end_minmin> = 16:31) - Change here if needed
    end_maxmin = 35         #Maximum Minute for randominzing Feierabend (16:<end_maxmin> = 16:35) - Change here if needed
    start_time = 0           # 08:30 gets updated within daily while loop
    end_time = 0             # 16:15 gets updated within daily while loop
    start_mintime = 0        # dt(start_time.year, start_time.month, start_time.day, start_time.hour, start_minmin)
    start_maxtime = 0        # dt(start_time.year, start_time.month, start_time.day, start_time.hour, start_maxmin)
    end_mintime = 0         
    end_maxtime = 0
    @classmethod
    def update(self):
        x = dt.now()
        self.start_time = dt(x.year, x.month, x.day, 8, 30)
        self.end_time = dt(x.year, x.month, x.day, 16, 15)
        self.start_mintime = dt(self.start_time.year, self.start_time.month, self.start_time.day, self.start_time.hour, self.start_minmin)
        self.start_maxtime = dt(self.start_time.year, self.start_time.month, self.start_time.day, self.start_time.hour, self.start_maxmin)
        self.end_mintime = dt(self.end_time.year, self.end_time.month, self.end_time.day, self.end_time.hour, self.end_minmin)
        self.end_maxtime = dt(self.end_time.year, self.end_time.month, self.end_time.day, self.end_time.hour, self.end_maxmin)

def Datum():
    print(f"{dt.now().isoformat()}")

def ZE_get(browser):
    # gets status (bool: True = running) and timestamps (string: in %H:%M [if available]) of Zeiterfassung
    # called by ZE.update class-method from ZE.class
    browser.get(link.home)
    Block = browser.find_element(By.CLASS_NAME, "card-text.content.mt-3")
    if Block.text.split("\n")[0][-1].isdigit():
        startzeitstr = Block.text.split("\n")[0]
        startzeit = startzeitstr[-5:]
        if Block.text.split("\n")[1][-1].isdigit():
            endzeitstr = Block.text.split("\n")[1]
            endzeit = endzeitstr[-5:]
            status = False
        else:
           endzeit = 'NaN'
           status = True
    else:
        startzeit = 'NaN'
        endzeit = 'NaN'
        status = False
    return status, startzeit, endzeit

def RandStartZeit():
    now = dt.now()
    if now < times.start_mintime:
        randi = dt(now.year,now.month,now.day,8,randint(times.start_minmin,times.start_maxmin))
    elif now > times.start_mintime and now < times.start_maxtime:
        randi = dt(now.year,now.month,now.day,8,randint(now.minute,times.start_maxmin))
    else:
        randi = now + td(seconds=5)
    return randi

def RandEndZeit():
    now = dt.now()
    if now >= times.end_mintime:
        randi = dt(now.year,now.month,now.day,16,randint((now.minute),times.end_maxmin))
    else:
        randi = dt(now.year,now.month,now.day,16,randint(times.end_minmin,times.end_maxmin))
    return randi

def zeStart(home):
    print("Starting...")
    browser.get(link.home)
    elements = browser.find_element(By.CLASS_NAME, 'card-body.p-3')
    ssbutton = elements.find_element(By.CLASS_NAME, 'btn-primary')
    if not ssbutton.is_displayed():
        browser.find_element(By.ID, "sidepreopen-control").click()
        if not ssbutton.is_displayed():
            return f'Error'
    try:
        selection = elements.find_elements(By.CLASS_NAME, 'form-check-input')
        homeofficebox = selection[0]
        standortbox = selection[-1]
    except NoSuchElementException:
        print(f'Selection failed because there was no selection when trying to start.')
    except IndexError:
        print(f"Selection failed because I couldn't select.")
    except:
        print(f"Selection failed because something went wrong.")
    else:
        if home == True:
            homeofficebox.click()
            print("You will be erfasst at Homeoffice.")
            sleep(1)
        else:
            standortbox.click()
            print("You will be erfasst at Standort.")

    if ssbutton.get_attribute("value") == "Starten":
        try:
            ssbutton.click()
            jetzt = dt.now()
            sleep(0.5)
        except:
            print("Something went wrong (EX). Please check your Zeiterfassung manualy.")
        else:
            if browser.current_url == link.zestarted:
                print(f"Zeiterfassung started at {jetzt.isoformat()}.")
                state = True
            else:
                print("Something went wrong. Please check your Zeiterfassung manualy.")
                state = False
        finally:
            return state
    else:
        print("Something went wrong while getting the 'Starten'-button.")
        if ssbutton.text() == 'Beenden':
            return f'Zeiterfassung already running.'

def zeEnde(browser):
    print("Stopping...")
    browser.get(link.home)
    sleep(1)
    elements = browser.find_element(By.CLASS_NAME, 'mt-3')
    button = elements.find_element(By.CLASS_NAME, 'btn-primary')
    if button.text == "Beenden":
        if not button.is_displayed():
            browser.find_element(By.ID, "sidepreopen-control").click()
            if not button.is_displayed():
                return f'Error'
        try:
            button.click()
            jetzt = dt.now()
            sleep(1)
            if browser.current_url == link.zestopped:
                print(f"Zeiterfassung stopped at {jetzt.isoformat()}.")
                state = True
            else:
                print("Something went wrong. Please check your Zeiterfassung manualy.")
                state = False
        except:
            print("Something went wrong (EX). Please check your Zeiterfassung manualy.")
    else:
        print("Something went wrong while getting the 'Beenden'-button.")
        state = False
    return state

def SleepUntilNextDay():
    # Sleep until next Day 7:58 AM
    now = dt.now()
    tomorrow = dt(now.year, now.month, (now.day + 1), 7, 58)
    delta = tomorrow - now
    time = delta.total_seconds()
    print(f"Sleeping until {tomorrow.isoformat()} .. or T-{time/60:.2f} minutes")
    sleep(time)

def SleepUntilFeierabend():
    # Sleeps until 15 minutes before Feierabend
    now = dt.now()
    until = times.end_time
    delta = until - now
    secs = delta.total_seconds()
    for i in range(round(secs),2,-1):
        print(f"Sleeping until {until.isoformat()} or {i} seconds.         ", end="\r")
        sleep(0.995)
    print("                                                                ", end="\r")
    print("Waking up.    ", end="\r")
    sleep(0.99)
    print("Waking up..   ", end="\r")
    sleep(0.99)
    #sleep(time)

def HomeOrNot(): #returns True for home or False for Standort and boolean for daily selection between home or not 
    while True:
        wo = input("1 = Homeoffice or 2 = Standort: ")
        match wo:
            case "1":
                home = True
                break
            case "2":
                home = False
                break
            case _:
                print("Wrong input. Choose between 1 = Homeoffice and 2 = Standort.")
                continue
    YN = input("Would you like to save your selection? (Y/N)")
    if YN.lower() == "y":
        while True:
            num = input("Enter the number of days, the selection should be saved for (not including today): ")
            if num.isdigit():
                days = int(num)
                if 1 <= days <= 180:
                    break
                print("Wrong input. Choose a number in range from 1 to 180")
    else:
        days = 0
    return home, days

def saveSelection(days: int) -> list:
    todaysindex = ondays.index(dt.today().strftime("%Y/%m/%d"))
    savedSelection_days = []
    for day in range(1,days+1):
        savedSelection_days.append(ondays[todaysindex+day])
    return savedSelection_days

def main():
    useri, passi = enter_creds()
    # logged_in = login_user(browser, useri, passi)
    home, days = HomeOrNot()
    if days > 0:
        saveSelection(days)
    dates = ondays
    # name = getFullName(browser)
    while True:
        clear()
        x = dt.now()
        date = x.strftime("%Y/%m/%d")
        if date in dates:
            print("Theres gonna be a Zeiterfassung today! Going into Zeiterfassungs-Modus.")
            ZE.reason = True
        else:
            print("Theres no Zeiterfassung for today. Going to sleep...")
            ZE.reason = False
            ZE.done = True
            SleepUntilNextDay()
            continue

        # Next part is only run, when date in dates (ZE.reason = True).

        logged_in = login_check(browser)
        
        if not logged_in:
            logged_in = login_user(browser, useri, passi)

        while logged_in:
            now = dt.now()
            Datum()
            times.update()
            ZE.update(browser)
            if ZE.startzeitstr[-1].isdigit() is True:
                startstring = ZE.startzeitstr
                if ZE.endzeitstr[-1].isdigit() is True:
                    endstring = ZE.endzeitstr
                    print(f'Zeiterfassung started at {startstring} and stopped at {endstring}.')
                    ZE.done = True
                else:   
                    print(f'Zeiterfassung started at {startstring}.')
                    ZE.done = False
            sleep(0.99)

            if ZE.running == False and now < times.start_time:
                Starten = True
                print("Zeiterfassung will be started soon.")
            else:
                Starten = False

            while Starten:
                now = dt.now()
                randtime = RandStartZeit()
                delta = randtime - now
                sleeptime = delta.total_seconds()
                if sleeptime > 9: 
                    print(f'Starting Zeiterfassung at {randtime.isoformat()}')
                    print(f"Sleeping for {sleeptime} seconds.                     ", end="\r")
                    sleep(sleeptime)
                    print("                                                    ", end="\r")
                else:
                    print(f'Seems like were running late today...')
                    print(f"Starting in {sleeptime} seconds.                   ", end="\r")
                    sleep(sleeptime)
                    print("                                                    ", end="\r")
                status = zeStart(home)
                if status == True:
                    print("Success.")
                    ZE.done = False
                    ZE.running = True
                    break
                else:
                    print("Something went wrong while starting the Zeiterfassung.")
                    ZE.done = False
                    ZE.running = False
                    break

            if ZE.running == True and now >= times.end_time:
                # When ZE is running and now is bigger or equal to 16:15
                Stoppen = True
                print("Zeiterfassung will be stopped soon.")
            else:
                Stoppen = False

            while Stoppen:
                now = dt.now()
                randtime = RandEndZeit()
                delta = randtime - now
                sleeptime = delta.total_seconds()
                if sleeptime > 9: 
                    print(f'Stopping Zeiterfassung at {randtime.isoformat()}')
                    print(f"Sleeping for {sleeptime} seconds.             ", end="\r")
                    sleep(sleeptime)
                    print("                                                    ", end="\r")
                else:
                    print(f'Seems like were running late today...')
                    print(f"Sleeping for {sleeptime} seconds.             ", end="\r")
                    sleep(sleeptime)
                    print("                                                    ", end="\r")
                stop = zeEnde(browser)
                if stop == True:
                    print("Success.")
                    ZE.done = True
                    ZE.running = False
                    break
                else:
                    print("Something went wrong while stopping the Zeiterfassung.")
                    ZE.done = True
                    ZE.running = False
                    break

            while not Stoppen and not Starten:
                # while not Starting (0800-0830) and Stopping (1630-) go sleep until next event
                # Sleep until Feierabend (1615)
                now = dt.now()
                feierabend = ZE.feierabend
                if ZE.running == True and now < feierabend:
                    print(f'Waiting for Feierabend.        ', end="\r")
                    sleep(0.9)
                    print(f'Waiting for Feierabend..       ', end="\r")
                    sleep(0.9)
                    print(f'Waiting for Feierabend...      ', end="\r")
                    sleep(0.9)
                    ZE.done = False
                    SleepUntilFeierabend()
                    break

                # Sleep until Start?
                elif ZE.running == False and ZE.done == True:
                    print(f"Seems like we're done for today.     ", end="\r")
                    sleep(0.9)
                    print(f"Seems like we're done for today..    ", end="\r")
                    sleep(0.9)
                    print(f"Seems like we're done for today...   ", end="\r")
                    sleep(0.9)
                    SleepUntilNextDay()
                    break
            
            if ZE.done == False:
                print(f"Refreshing..                             ")
                sleep(0.99)
                countdown(5)
                continue
            else:
                print(f"Restarting..                             ")
                sleep(0.99)
                countdown(5)
                break

if __name__ == "__main__":
    main(browser)
