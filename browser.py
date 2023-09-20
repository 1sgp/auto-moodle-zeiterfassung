from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoAlertPresentException
from bs4 import BeautifulSoup as bs
from time import sleep

def getLang(browser):
    return browser.find_element(By.TAG_NAME, "html").get_attribute('lang')

def setLang(browser, lang: str):
    browser.get(f"https://lernplattform.gfn.de/?lang={lang}")

class link:
    login = "https://lernplattform.gfn.de/login/index.php"
    home = "https://lernplattform.gfn.de/"
    zestarted = "https://lernplattform.gfn.de/?starten=1"
    zestopped = "https://lernplattform.gfn.de/?stoppen=1"

def init():
    options=Options()
    #options.add_argument('-headless')
    browser=webdriver.Firefox(options=options)
    return browser

def safeget(browser, link: str, x = 3):
    browser.get(link)
    sleep(x)
    # handleAlert()
    # handleDatapref()

def getFullName(browser):
    status = login_check(browser)
    if status:
        try:
            str = browser.find_element(By.CLASS_NAME, "box.py-3.modal-body").text
        except:
            pass
        else:
            if str.lower().startswith("y"):
                strEN = str.split(",")[0].split()[6:]
                strEN[0].split()[6:]
                fullname = " ".join(strEN)
            
            if str.lower().startswith("s"):
                strDE = str.split("angemeldet")[0].split()[4:]
                fullname = " ".join(strDE)
    else:
        pass
    return fullname

def handleAlert(browser):
    # For future implementation
    try:
        browser.switch_to.alert.dismiss()
        browser.switch_to.alert.accept()
    # except TimeoutException:
    #     pass
    # except NoSuchElementException:
    #     pass
    # except NoAlertPresentException:
    #     pass
    except:
        pass

def handleDatapref(browser):
    # For future implementation
    try:
        pref = browser.find_element(By.CLASS_NAME, "modal-dialog-scrollable")
    except TimeoutException:
        pass
    except NoSuchElementException:
        pass
    else:
        pref.find_element(By.TAG_NAME, "button").click()

def login_check(browser: object):
    browser.get(link.login)
    sindbereitsDE = "Sie sind bereits"
    sindbereitsEN = "You are already"
    if sindbereitsDE in browser.page_source or sindbereitsEN in browser.page_source:
        return True
    if browser.find_element(By.CLASS_NAME, 'btn.btn-primary').text == "Login":
        return False
    return False

def login_user(browser: object, User: str, Pass: str):
    browser.get(link.login)
    try:
        username = browser.find_element(By.ID, 'username')
        password = browser.find_element(By.ID, 'password')
        loginbut = browser.find_element(By.CLASS_NAME, 'btn-primary')
    except NoSuchElementException:
        return True
    except Exception as e:
        return False, f'Error: {type(e).__name__}'
    print("Logging in ..")
    username.clear()
    username.send_keys(User)
    password.clear()
    password.send_keys(Pass)
    loginbut.click()
    ungueltigDE = "Ungültige Anmeldedaten. Versuchen Sie es noch einmal!"
    ungueltigEN = "Invalid login, please try again"
    handleAlert(browser)
    handleDatapref(browser)
    if ungueltigDE in browser.page_source or ungueltigEN in browser.page_source:
        return False, f"Wrong credentials."
    return True