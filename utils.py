# utils

from datetime import datetime as dt
from datetime import timedelta as td
from getpass import getpass as gp
from os import name, system
from time import sleep
from random import randint

class Times:
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

def clear():
    system('cls' if name == 'nt' else 'clear')

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
    
def RandStartZeit():
    now = dt.now()
    if now < Times.start_mintime:
        randi = dt(now.year,now.month,now.day,8,randint(Times.start_minmin,Times.start_maxmin))
    elif now > Times.start_mintime and now < Times.start_maxtime:
        randi = dt(now.year,now.month,now.day,8,randint(now.minute,Times.start_maxmin))
    else:
        randi = now + td(seconds=3)
    return randi

def RandEndZeit():
    now = dt.now()
    if now >= Times.end_mintime:
        randi = dt(now.year,now.month,now.day,16,randint((now.minute),Times.end_maxmin))
    else:
        randi = dt(now.year,now.month,now.day,16,randint(Times.end_minmin,Times.end_maxmin))
    return randi
