from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

wait = lambda browser, x: WebDriverWait(browser, x)

class link:
    login = "https://lernplattform.gfn.de/login/index.php"
    home = "https://lernplattform.gfn.de/"
    my = "https://lernplattform.gfn.de/my/"
    zestarted = "https://lernplattform.gfn.de/?starten=1"
    zestopped = "https://lernplattform.gfn.de/?stoppen=1"

def init() -> object:
    options=Options()
    #options.add_argument('-headless')
    browser=webdriver.Firefox(options=options)
    return browser

def opensidepanel(browser) -> bool:
    if browser.find_element(By.ID, "sidepreopen-control").get_attribute("aria-expanded") == "false":
        browser.find_element(By.ID, "sidepreopen-control").click()
    return True

def openusermenu(browser) -> bool:
    if  browser.find_element(By.ID, 'action-menu-toggle-1').get_attribute('aria-expanded') == "false":
         browser.find_element(By.ID, 'action-menu-toggle-1').click()
    return True

def handleAlert(browser):
    # handles the reminder-alert for zeiterfassung - usually pops after first login of the day 
    try:
        browser.switch_to.alert.dismiss()
        browser.switch_to.alert.accept()
    except:
        pass

def handleDatapref(browser):
    # Tries to find the "Datenpräferenz"-Dialog and handle it
    try:
        pref = browser.find_element(By.CLASS_NAME, "modal-dialog-scrollable")
    except:
        pass
    else:
        pref.find_element(By.TAG_NAME, "button").click()

def login_check(browser: object) -> bool:
    browser.get(link.login)
    sindbereitsDE = "Sie sind bereits"
    sindbereitsEN = "You are already"
    if sindbereitsDE in browser.page_source or sindbereitsEN in browser.page_source:
        return True
    if browser.find_element(By.CLASS_NAME, 'btn.btn-primary').text == "Login":
        return False
    return False

def login_user(browser: object, User: str, Pass: str) -> bool:
    browser.get(link.login)
    try:
        username = browser.find_element(By.ID, 'username')
        password = browser.find_element(By.ID, 'password')
        loginbut = browser.find_element(By.CLASS_NAME, 'btn-primary')
    except:
        check = login_check(browser)
        return check
    username.clear()
    username.send_keys(User)
    password.clear()
    password.send_keys(Pass)
    loginbut.click()
    wait(browser, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "slicon-social-youtube")))
    ungueltigDE = "Ungültige Anmeldedaten. Versuchen Sie es noch einmal!"
    ungueltigEN = "Invalid login, please try again"
    if ungueltigDE in browser.page_source or ungueltigEN in browser.page_source:
        return False, f"Wrong credentials."
    handleAlert(browser)
    handleDatapref(browser)
    return True

def getStatus(browser) -> (bool, str, str):
    # gets status (bool: True = running) and timestamps (string: in %H:%M [if available]) of Zeiterfassung
    # called by ZE.update class-method from ZE.class
    browser.get(link.home)
    opensidepanel(browser)
    Block = browser.find_element(By.CLASS_NAME, "card-text.content.mt-3")
    startzeitstr = Block.text.split("\n")[0]
    startzeit = startzeitstr[-5:] if startzeitstr[-1].isdigit() else None
    endzeitstr = Block.text.split("\n")[1] if len(Block.text.split("\n")) > 1 else None
    endzeit = endzeitstr[-5:] if endzeitstr and endzeitstr[-1].isdigit() else None
    status = False if startzeit and endzeit else True
    return status, startzeit, endzeit

def Start(browser, home):
    browser.get(link.home)
    opensidepanel(browser)
    elements = browser.find_element(By.CLASS_NAME, 'card-body.p-3')
    startbutton = elements.find_element(By.CLASS_NAME, 'btn-primary')
    selection = elements.find_elements(By.CLASS_NAME, 'form-check-input')
    homeofficebox = selection[0]
    standortbox = selection[-1]
    if home:
        homeofficebox.click()
    else:
        standortbox.click()
    #startbutton.click()
    print(f'startbutton.click()')
    if browser.current_url == link.zestarted:
        return True
    else:
        return False

def Ende(browser):
    browser.get(link.home)
    opensidepanel(browser)
    #browser.find_element(By.CLASS_NAME, 'card-body.p-3').find_element(By.CLASS_NAME, 'btn-primary').click()
    print(f"browser.find_element(By.CLASS_NAME, 'card-body.p-3').find_element(By.CLASS_NAME, 'btn-primary').click()")
    if browser.current_url == link.zestopped:
        return True
    else:
        return False
