"""
    This code automates bulk activation of Steam keys.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import getpass

"""These instructions would read the username, password and Steam Guard code from bash."""
username = raw_input("Enter your username: ")
password = pw = getpass.getpass("Enter your password: ")
sgCode = raw_input("Enter your Steam Guard code: ")

"""Create a Firefox browser instance."""
driver = webdriver.Firefox()
delay = 5

"""Open the url of Steam login."""
driver.get("https://store.steampowered.com//login/")

"""Select the username text input."""
try:
    inputElement = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"input_username\"]")))
    """Insert the username into this input."""
    inputElement.send_keys(username)
except TimeoutException:
    print "Username -> Loading the element took too much time!"

"""Fulfill the password."""
try:
    inputElement = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"input_password\"]")))
    inputElement.send_keys(password)
except TimeoutException:
    print "Passrowd -> Loading the element took too much time!"

"""Click on the submit button to login."""
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"login_btn_signin\"]/button"))).click()
except TimeoutException:
    print "Login Button -> Loading the element took too much time!"

time.sleep(2)

"""Condition to distinguish between the Steam Guard of the mobile application and the Steam Guard that sends the code by email."""
if driver.find_element_by_xpath("//*[@id=\"twofactorcode_entry\"]").is_displayed():
    """Fulfill the steam guard code """
    try:
        inputElement = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"twofactorcode_entry\"]")))
        inputElement.send_keys(sgCode)
    except TimeoutException:
        print "Input Steam Guard (APP) -> Loading the element took too much time!"

    """Click on the submit button to login on Steam Guard."""
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"login_twofactorauth_buttonset_entercode\"]/div[1]"))).click() 
    except TimeoutException:
        print "Submit Steam Guard code (APP) -> Loading the element took too much time!"
        
else:
    """Fulfill the steam guard email code """
    try:
        inputElement = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"authcode\"]")))
        inputElement.send_keys(sgCode)
    except TimeoutException:
        print "Input Steam Guard (Email) -> Loading the element took too much time!"

    """Click on the submit button to login on Steam Guard email code."""
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"auth_buttonset_entercode\"]/div[1]"))).click()
        time.sleep(2)
    except TimeoutException:
        print "Submit Steam Guard code (Email) -> Loading the element took too much time!"

    """Click the button to confirm the success of the Steam Guard code sent to the email."""
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"success_continue_btn\"]"))).click() 
    except TimeoutException:
        print "Confirm Steam Guard (Email) -> Loading the element took too much time!"

time.sleep(5)

"""Condition to redirect to the key activation page after login is done."""
if driver.current_url == "http://store.steampowered.com/":
    driver.get("https://store.steampowered.com/account/registerkey")
    
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
