"""
    This code automates bulk activation of Steam keys.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import ui
import time
import pickle
import getpass
import sys
import os

def page_loaded(driver):
	return driver.find_element_by_tag_name("body") != None

def find_element_by_xpath(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except TimeoutException:
        print "Username -> Loading the element took too much time!"
        driver.quit()
        sys.exit(1)
    finally:
        return element

def find_element_by_id(driver, id):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, id))
        )
    except TimeoutException:
        print "Username -> Loading the element took too much time!"
        driver.quit()
        sys.exit(1)
    finally:
        return element

def xpath_element_is_displayed(driver, xpath):
    find_element_by_xpath(driver, xpath)
    return True

def wait_until_element_is_displayed(driver, element_xpath):
    counter = 0
    while(True):
        if driver.find_element_by_xpath(element_xpath).is_displayed():
            return find_element_by_xpath(driver, element_xpath)
        if counter > 15:
            return False
        
        counter+=1
        time.sleep(1)

def login_part_two(driver, username, password):
    driver.get("https://store.steampowered.com/login/")

    inputElement = find_element_by_xpath(driver, "//*[@id=\"input_username\"]")
    inputElement.send_keys(username)

    inputElement = find_element_by_xpath(driver, "//*[@id=\"input_password\"]")
    inputElement.send_keys(password)
    
    remember_login_button = find_element_by_id(driver, 'remember_login')
    remember_login_button.click()
    
    login_button = find_element_by_xpath(driver, "//*[@id=\"login_btn_signin\"]/button")
    login_button.click()

def login_part_one(driver, username, password):
    inputElement = find_element_by_xpath(driver, "//*[@id=\"input_username\"]")
    inputElement.send_keys(username)

    inputElement = find_element_by_xpath(driver, "//*[@id=\"input_password\"]")
    inputElement.send_keys(password)

    login_button = find_element_by_xpath(driver, "//*[@id=\"login_btn_signin\"]/button")
    login_button.click()

    sgCode = raw_input("Enter your Steam Guard code: ")

    if driver.find_element_by_xpath("//*[@id=\"twofactorcode_entry\"]").is_displayed():

        inputElement = find_element_by_xpath(driver, "//*[@id=\"twofactorcode_entry\"]")
        inputElement.send_keys(sgCode)
        
        button = find_element_by_xpath(driver, "//*[@id=\"login_twofactorauth_buttonset_entercode\"]/div[1]")
        button.click()
    
    else:
        inputElement = find_element_by_xpath(driver, "//*[@id=\"authcode\"]")
        inputElement.send_keys(sgCode)

        button = find_element_by_xpath(driver, '//*[@id=\"auth_buttonset_entercode\"]/div[1]')
        button.click()

        button = wait_until_element_is_displayed(driver, "//*[@id=\"success_continue_btn\"]")
        button.click()

def login_with_cookies(driver):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get("https://store.steampowered.com/account/registerkey")
    wait = ui.WebDriverWait(driver, 10)
    wait.until(page_loaded)

    if driver.current_url == "https://store.steampowered.com/account/registerkey":
        return True

    return False

def login(driver, username, password):
    driver.get("https://store.steampowered.com/login/")
    wait = ui.WebDriverWait(driver, 10)
    wait.until(page_loaded)

    if os.path.exists("cookies.pkl"):
        if login_with_cookies(driver):
            return
    
    login_part_one(driver, username, password)
    driver.execute_script('Logout();')
    wait = ui.WebDriverWait(driver, 10)
    wait.until(page_loaded)

    login_part_two(driver, username, password)
    wait = ui.WebDriverWait(driver, 10)
    wait.until(page_loaded)

    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

reload(sys)
sys.setdefaultencoding('utf-8')

username = raw_input("Enter your username: ")
password = pw = getpass.getpass("Enter your password: ")

driver = webdriver.Chrome()
login(driver, username, password)

delay = 10
driver.get("https://store.steampowered.com/account/registerkey")
wait = ui.WebDriverWait(driver, 10)
wait.until(page_loaded)

"""Click on the acceptance box for the terms of the service."""
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"accept_ssa\"]"))).click() 
except TimeoutException:
    print "Acceptance Box -> Loading the element took too much time!"

"""Cycle to read the keys of a file and activate one by one in the Steam."""
ref_arquivo = open("keys.txt","r")
linha = ref_arquivo.readline()
while linha:
    """Select the key text input."""
    try:
        inputElement = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"product_key\"]")))
        inputElement.send_keys(linha)
    except TimeoutException:
        print "Input Key -> Loading the element took too much time!"

    """Click on the button to activate the key."""
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"register_btn\"]"))).click()
        time.sleep(1)
    except TimeoutException:
        print "Button to activate the key -> Loading the element took too much time!"

    """Condition to check if an error occurred activating the key."""
    if driver.find_element_by_xpath("//*[@id=\"error_display\"]").is_displayed():
        try:
            activationError = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"error_display\"]")))
            print("\n" + activationError.text + " (" + linha.rstrip() + ")")
        except TimeoutException:
            print "Game Name -> Loading the element took too much time!"

        """Clears the textbox where the keys are placed."""
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"product_key\"]"))).clear() 
        except TimeoutException:
            print "Text Area Keys (Clear) -> Loading the element took a long time!"

    else:
        """Game confirmation enabled"""
        try:
            gameName = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"registerkey_productlist\"]/div")))
            print("\nSuccessfully activated: " + gameName.text + " (" + linha.rstrip() + ")")
        except TimeoutException:
            print "Game Name -> Loading the element took too much time!"
            
        """Click on the button to return to the activate keys page."""
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"receipt_form\"]/div[3]/a[1]"))).click() 
        except TimeoutException:
            print "Button to return key activation page -> Loading the element took a long time!"

        """Click on the acceptance box for the terms of the service."""
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"accept_ssa\"]"))).click() 
        except TimeoutException:
            print "Acceptance Box -> Loading the element took a long time!"
        
    linha = ref_arquivo.readline()
    
ref_arquivo.close()

driver.close()
