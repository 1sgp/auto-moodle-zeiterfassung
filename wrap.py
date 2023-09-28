# wrap

from time import sleep
from browser import init as init
from browser import login_user, handleAlert, handleDatapref, wait, getStatus, opensidepanel, Start, Ende
from browser import link as link
from utils import clear, Times, RandStartZeit, RandEndZeit
from datetime import datetime as dt

def main(user: str, word: str):
    clear()
    print(f'Go go go!')
    browser = init()
    while True:
        Times.update()
        login_user(browser, user, word)
        status, start, ende = getStatus(browser)

        if status != True and ende == None:
            Startzeit = RandStartZeit()
            delta = round((Startzeit - dt.now()).total_seconds(), 0)
            # if delta > 600:
            #     continue
            print(f'Going to sleep for {delta} seconds.')
            browser.quit()
            sleep(delta)
            browser = init()
            Start(browser)
            return True, f'Start: {Startzeit.isoformat()}'
        
        if status == True and ende == None:
            Endzeit = RandEndZeit()
            delta = round((Endzeit - dt.now()).total_seconds(), 0)
            print(f'Going to sleep for {delta} seconds.')
            browser.quit()
            # if delta > 600:
            #     continue
            sleep(delta)
            browser = init()
            Ende(browser)
            return True, f'Ende: {Endzeit.isoformat()}'
        
        if status == True and ende != None:
            break
    browser.quit()
    return True, f'Nothing to do!', f'Start: {start}', f'Ende: {ende}'