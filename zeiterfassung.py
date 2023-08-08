from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from datetime import timedelta as td
from getpass import getpass as gp
from os import system, name
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep

options=Options()
options.add_argument('-headless')
browser=webdriver.Firefox(options=options)

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def newsleeps(x):
    now = dt.now()
    if type(x) == str:
        untiltime = dt.strptime(x, '%H:%M')
        until = dt(now.year, now.month, now.day, untiltime.hour, untiltime.minute)
        delta = (untiltime - now).total_seconds()
        x = round(delta)
    else:
        delta = td(seconds=x)
        until = now + delta
    # delta = dt(now.year, now.month, now.day, now.hour, now.minute, now.second)
    for i in range(x,1,-1):
        print(f"Sleeping until {until.isoformat()} or {i} seconds.         ", end="\r")
        sleep(0.995)
    print(f"Sleeping until {until.isoformat()} or 1 second.                   ", end="\r")
    sleep(0.995)
    print(f"                                                                      ", end="\r")

class link:
    login = "https://lernplattform.gfn.de/login/index.php"
    home = "https://lernplattform.gfn.de/"
    zestarted = "https://lernplattform.gfn.de/?starten=1"
    zestopped = "https://lernplattform.gfn.de/?stoppen=1"

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
    def update(self):
        status, started, stopped = ZE_get()
        self.now = dt.now()
        self.running = status
        self.startzeitstr = started
        self.endzeitstr = stopped
        self.startzeit = dt.strptime(started, '%H:%M') if started[-1].isdigit() is True else "NaN"
        self.endzeit = dt.strptime(stopped, '%H:%M') if stopped[-1].isdigit() is True else "NaN"

class times:
    start_minmin = 19        #Minimum Minute for randominzing Start (8:<start_minmin> = 8:00) - Change here if needed - ex.: set to 15 for a random login time between 8:15 and 8:30. (default 0)
    start_maxmin = 30       #Minimum Minute for randominzing Start (8:<start_maxmin> = 8:30) - Change here if needed - ex.: set to 15 for a random login time between 8:00 and 8:15. (default 30)
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
        self.startmintime = dt(self.start_time.year, self.start_time.month, self.start_time.day, self.start_time.hour, self.start_minmin)
        self.startmaxtime = dt(self.start_time.year, self.start_time.month, self.start_time.day, self.start_time.hour, self.start_maxmin)
        self.endmintime = dt(self.start_time.year, self.start_time.month, self.start_time.day, self.start_time.hour, self.end_minmin)
        self.endmaxtime = dt(self.start_time.year, self.start_time.month, self.start_time.day, self.start_time.hour, self.end_maxmin)


def countdown(secs):
    for i in range(secs,1,-1):
        print(f"{i} seconds left until refreshing..", end="\r")
        realsleep = 1 - 0.01
        sleep(realsleep)
    print(f"Refreshing in 1 second.                ", end="\r")
    sleep(0.99)

def Datum():
    print(f"{now.isoformat()}")

def enter_creds():
    print("Please enter your credentials. You may correct them, when the login doesn't work.")
    User = input('Username: ')
    Pass = gp(prompt='Password: ')
    if User == "":
        print('Please enter a username.')
        User = input('Username: ')
    elif Pass == "":
        Pass = gp(prompt='Please enter a password: ')
    else:
        print('Credentials accepted.')
    sleep(0.99)
    clear()
    return User, Pass

def check_creds(User, Pass):
    if User == "":
        User = input('Username: ')
    else:
        print('Username: ', User)
        changeit = input('Do you want to change the username? (Y/N):')
        if changeit.lower() == "y":
            User = input('Username: ')
            clear()
            print(User)
    if Pass == "":
        print('Please enter a valid password')
        Pass = gp(prompt='Enter a password please: ')
    else:
        pwc = input('Do you want to VISIBLY check your password? (Y/N):')
    if pwc.lower() == "y":
        print('Username: ', User)
        print('Password: ', Pass)
        sleep(3)
        clear()
    pwr = input('Do you want to change your password? (Y/N):')
    if pwr.lower() == "y":
        Pass = gp(prompt='Enter a new password please: ')      
    return User, Pass

def login_user(User, Pass):
    logged_in = login_check()
    if logged_in == False:
        try:
            browser.get(link.login)
            username = browser.find_element(By.ID, 'username')
            password = browser.find_element(By.ID, 'password')
            loginbut = browser.find_element(By.CLASS_NAME, 'btn-primary')
            print("Logging in ..")
            username.clear()
            username.send_keys(User)
            password.clear()
            password.send_keys(Pass)
            loginbut.click()
            sleep(1)
            if "Ungültige Anmeldedaten. Versuchen Sie es noch einmal!" in browser.page_source:
                print("Wrong credentials. Please check your input!")
                User, Pass = check_creds(User, Pass)
                sleep(2)
                login_user(User, Pass)
            else:
                logged_in = True
                print('Logged in!')
                return
        except NoSuchElementException:
            print('Error. Already signed in.')
            logged_in = True
        else:
            logged_in = True
            try:
                WebDriverWait(browser, 5).until(EC.alert_is_present(), 'No alerts around.')
                alert = browser.switch_to.alert
                alert.accept()
            except:
                return
        finally:
            return logged_in
    else:
        print('Already signed in.')
        logged_in = True
        return logged_in

def login_check():
    browser.get(link.login)
    sleep(0.99)
    try:
        username = browser.find_element(By.ID, 'username')
    except NoSuchElementException:
        if "Sie sind bereits als" in browser.page_source:
            logged_in = True
        else:
            print("This shouldn't have happened.")
            sleep(0.99)
            exit()
    except:
        print("Something went wrong.")
        sleep(0.99)
        exit()
    else:
        logged_in = False
    finally:
        return logged_in

def ZE_get():
    # gets status (bool: True = running) and timestamps (string: in %H:%M [if available]) of Zeiterfassung
    # called by update class-method from ZE.class
    browser.get(link.home)
    soup = bs(browser.page_source, 'html.parser')
    Block = soup.h5.parent
    zeiten = Block('p')
    if zeiten == None:
        startzeit = 'NaN'
        endzeit = 'NaN'
        status = False
        return status, startzeit, endzeit
    else:
        startzeitstr = Block('p')[0].text
        startzeit = startzeitstr[-5:]
        try:
            endzeitstr = Block('p')[1].text
            endzeit = endzeitstr[-5:]
        except IndexError:
            endzeit = 'NaN'
            status = True
        except:
            startzeit, endzeit = 'Error'
        else:
            status = False
        finally:
            return status, startzeit, endzeit

def RandStartZeit():
    now = dt.now()
    if now < times.startmintime:        #8:19
        randi = dt(now.year,now.month,now.day,8,randint(times.start_minmin,times.start_maxmin))
        randi = dt(now.year,now.month,now.day,8,randint((now.minute),times.start_maxmin))
    if randi < now: # If too late add 1 minute to now
        randi = dt(now.year,now.month,now.day,8,now.minute+1)
    return randi

def RandEndZeit():
    now = dt.now()
    if now.minute >= 30:
        randi = dt(now.year,now.month,now.day,16,randint((now.minute),times.end_maxmin))
    else:
        randi = dt(now.year,now.month,now.day,16,randint(30,times.end_maxmin))
    return randi

def zeStart():
    print("Starting...")
    browser.get(link.home)
    sleep(1)
    elements = browser.find_element(By.CLASS_NAME, 'mt-3')
    ssbutton = elements.find_element(By.CLASS_NAME, 'btn-primary')
    try:
        selection = elements.find_elements(By.CLASS_NAME, 'form-check-input')
        homeofficebox = selection[0]
        standortbox = selection[-1]
    except NoSuchElementException:
        print(f'Selection failed because there was no selection when trwrying to start.')
    except IndexError:
        print(f"Selection failed because I couldn't select.")
    except:
        print(f"Selection failed because something went wrong.")
    else:
        if home == True:
            homeofficebox.click()
            print("You will be erfasst at Homeoffice.")
        else:
            standortbox.click()
            print("You will be erfasst at Standort.")

    if ssbutton.text == "Starten":
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

def zeEnde():
    print("Stopping...")
    browser.get(link.home)
    sleep(1)
    elements = browser.find_element(By.CLASS_NAME, 'mt-3')
    button = elements.find_element(By.CLASS_NAME, 'btn-primary')
    if button.text == "Beenden":
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
    time = delta.total_seconds()
    for i in range(round(time),2,-1):
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
    return home
    

useri, passi = enter_creds()
logged_in = login_user(useri, passi)
home = HomeOrNot()
dates = ('2023/06/19', '2023/06/20', '2023/06/21', '2023/06/22', '2023/06/23', '2023/06/26', '2023/06/27', '2023/06/28', '2023/06/29', '2023/06/30', '2023/07/03', '2023/07/04', '2023/07/05', '2023/07/06', '2023/07/07', '2023/07/10', '2023/07/11', '2023/07/12', '2023/07/13', '2023/07/14', '2023/07/17', '2023/07/18', '2023/07/19', '2023/07/20', '2023/07/21', '2023/08/07', '2023/08/08', '2023/08/09', '2023/08/10', '2023/08/11', '2023/08/14', '2023/08/16', '2023/08/17', '2023/08/18', '2023/08/21', '2023/08/22', '2023/08/23', '2023/08/24', '2023/08/25', '2023/08/28', '2023/08/29', '2023/08/30', '2023/08/31', '2023/09/01', '2023/09/04', '2023/09/05', '2023/09/06', '2023/09/07', '2023/09/08', '2023/09/11', '2023/09/12', '2023/09/13', '2023/09/14', '2023/09/15', '2023/09/18', '2023/09/19', '2023/09/20', '2023/09/21', '2023/09/22', '2023/09/25', '2023/09/26', '2023/09/27', '2023/09/28', '2023/09/29', '2023/10/02', '2023/10/04', '2023/10/05', '2023/10/06', '2023/10/09', '2023/10/10', '2023/10/11', '2023/10/12', '2023/10/13', '2023/10/16', '2023/10/17', '2023/10/18', '2023/10/19', '2023/10/20', '2023/10/23', '2023/10/24', '2023/10/25', '2023/10/26', '2023/10/27', '2023/10/30', '2023/11/02', '2023/11/03', '2023/11/06', '2023/11/07', '2023/11/08', '2023/11/09', '2023/11/10', '2023/11/13', '2023/11/14', '2023/11/15', '2023/11/16', '2023/11/17', '2023/11/20', '2023/11/21', '2023/11/22', '2023/11/23', '2023/11/24', '2023/11/27', '2023/11/28', '2023/11/29', '2023/11/30', '2023/12/01', '2023/12/04', '2023/12/05', '2023/12/06', '2023/12/07', '2023/12/08', '2023/12/11', '2023/12/12', '2023/12/13', '2023/12/14', '2023/12/15', '2023/12/18', '2023/12/19', '2023/12/20', '2023/12/21', '2023/12/22', '2024/01/08', '2024/01/09', '2024/01/10', '2024/01/11', '2024/01/12', '2024/01/15', '2024/01/16', '2024/01/17', '2024/01/18', '2024/01/19', '2024/01/22', '2024/01/23', '2024/01/24', '2024/01/25', '2024/01/26', '2024/01/29', '2024/01/30', '2024/01/31', '2024/02/01', '2024/02/02', '2024/02/05', '2024/02/06', '2024/02/07', '2024/02/08', '2024/02/09', '2024/02/12', '2024/02/13', '2024/02/14', '2024/02/15', '2024/02/16', '2024/02/19', '2024/02/20', '2024/02/21', '2024/02/22', '2024/02/23', '2024/02/26', '2024/02/27', '2024/02/28', '2024/02/29', '2024/03/01', '2024/03/04', '2024/03/05', '2024/03/06', '2024/03/07', '2024/03/11', '2024/03/12', '2024/03/13', '2024/03/14', '2024/03/15', '2024/03/18', '2024/03/19', '2024/03/20', '2024/03/21', '2024/03/22', '2024/04/08', '2024/04/09', '2024/04/10', '2024/04/11', '2024/04/12', '2024/04/15', '2024/04/16', '2024/04/17', '2024/04/18', '2024/04/19', '2024/04/22', '2024/04/23', '2024/04/24', '2024/04/25', '2024/04/26', '2024/04/29', '2024/04/30', '2024/05/02', '2024/05/03', '2024/05/06', '2024/05/07', '2024/05/08', '2024/05/10', '2024/05/13', '2024/05/14', '2024/05/15', '2024/05/16', '2024/05/17', '2024/05/21', '2024/05/22', '2024/05/23', '2024/05/24', '2024/05/27', '2024/05/28', '2024/05/29', '2024/05/31', '2024/06/03', '2024/06/04', '2024/06/05', '2024/06/06', '2024/06/07', '2024/06/10', '2024/06/11', '2024/06/12', '2024/06/13', '2024/06/14', '2024/06/17', '2024/06/18', '2024/06/19', '2024/06/20', '2024/06/21', '2024/06/24', '2024/06/25', '2024/06/26', '2024/06/27', '2024/06/28', '2024/07/01', '2024/07/02', '2024/07/03', '2024/07/04', '2024/07/05', '2024/07/08', '2024/07/09', '2024/07/10', '2024/07/11', '2024/07/12', '2024/07/15', '2024/07/16', '2024/07/17', '2024/07/18', '2024/07/19', '2024/08/05', '2024/08/06', '2024/08/07', '2024/08/08', '2024/08/09', '2024/08/12', '2024/08/13', '2024/08/14', '2024/08/16', '2024/08/19', '2024/08/20', '2024/08/21', '2024/08/22', '2024/08/23', '2024/08/26', '2024/08/27', '2024/08/28', '2024/08/29', '2024/08/30', '2024/09/02', '2024/09/03', '2024/09/04', '2024/09/05', '2024/09/06', '2024/09/09', '2024/09/10', '2024/09/11', '2024/09/12', '2024/09/13', '2024/09/16', '2024/09/17', '2024/09/18', '2024/09/19', '2024/09/20')


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

    # times.start_time = dt(x.year, x.month, x.day, 8, 30)
    # times.end_time = dt(x.year, x.month, x.day, 16, 15)
    # replaced with times.update() in while loop

    logged_in = login_user(useri,passi)

    while logged_in:
        now = dt.now()
        Datum()
        times.update()
        ZE.update()
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
            print(f'Starting Zeiterfassung at {randtime.isoformat()}')
            sleep((sleeptime-1))
            status = zeStart()
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
            print(f'Stopping Zeiterfassung at {randtime.isoformat()}')
            print(f"Sleeping for {sleeptime-1} seconds.         ", end="\r")
            sleep((sleeptime-1))
            stop = zeEnde()
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
