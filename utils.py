# utils

from datetime import datetime as dt
from datetime import timedelta as td
from getpass import getpass as gp
from os import name, system
from time import sleep, time

def clear():
    system('cls' if name == 'nt' else 'clear')

def countdown(x):
    # A countdown that accepts seconds or a time in "HH:MM"-format as input.
    s = time()                  # Test
    now = dt.now()
    if type(x) == str:
        untiltime = dt.strptime(x, '%H:%M')
        until = dt(now.year, now.month, now.day, untiltime.hour, untiltime.minute)
        delta = (until - now).total_seconds()
        x = round(delta)
    else:
        delta = td(seconds=x)
        until = now + delta
    for i in range(x,1,-1):
        print(f"Sleeping until {until.isoformat()} or {i} seconds.         ", end="\r")
        sleep(0.995)
    print(f"Sleeping until {until.isoformat()} or 1 second.                   ", end="\r")
    sleep(0.995)
    print(f"                                                                      ", end="\r")
    print(f"Done after {time()-s:.2f} seconds")         # Test

def enter_creds():
    # Prompts for Credentials. name@domain.tld and a password with a minimum length of four (non-blank) characters
    # Used in terminal-application
    print("Please enter your credentials. You may correct them, when the login doesn't work.")
    i = 0
    while i < 5:
        User = input("Username: ")
        if User.strip() == "" or "@" not in str(User):
            print("Please enter a valid username. [name@domain.tld]")
            i+=1
        else:
            break
    if i == 5:
            return f"Exceeded maximum tries. Please do better next time!"
    else:
        pass
    i = 0
    while i < 5:
        Pass = gp(prompt='Password: ')
        if len(Pass.strip()) <= 4:
            print("Please enter a valid password.")
            Pass = ""
            i+=1
        else:
            break
    if i < 5:
        print("Credentials accepted.")
        return User, Pass
    else:
        return f"Exceeded maximum tries. Please do better next time!"