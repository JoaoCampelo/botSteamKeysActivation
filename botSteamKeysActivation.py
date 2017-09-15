"""
    This code automates bulk activation of Steam keys.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import getpass

"""These instructions would read the username, password and Steam Guard code from bash."""
username = raw_input("Enter your username: ")
password = pw = getpass.getpass("Enter your password: ")
sgCode = raw_input("Enter your Steam Guard code: ")

"""Create a Firefox browser instance."""
driver = webdriver.Firefox()

"""Open the url of Steam login."""
driver.get("https://store.steampowered.com//login/")
driver.implicitly_wait(3)

"""Select the username text input."""
inputElement = driver.find_element_by_xpath("//*[@id=\"input_username\"]")
"""Insert the username into this input."""
inputElement.send_keys(username)
time.sleep(1)

"""Fulfill the password."""
inputElement = driver.find_element_by_xpath("//*[@id=\"input_password\"]")
inputElement.send_keys(password)
time.sleep(1)

"""Click on the submit button to login."""
driver.find_element_by_xpath("//*[@id=\"login_btn_signin\"]/button").click()
time.sleep(2)

"""Condition to distinguish between the Steam Guard of the mobile application and the Steam Guard that sends the code by email."""
if driver.find_element_by_xpath("//*[@id=\"twofactorcode_entry\"]").is_displayed():
	"""Fulfill the steam guard code """
	inputElement = driver.find_element_by_xpath("//*[@id=\"twofactorcode_entry\"]")
	inputElement.send_keys(sgCode)
	time.sleep(1)

	"""Click on the submit button to login on Steam Guard."""
        driver.find_element_by_xpath("//*[@id=\"login_twofactorauth_buttonset_entercode\"]/div[1]").click()
        time.sleep(3)
        
else:
        """Fulfill the steam guard email code """
	inputElement = driver.find_element_by_xpath("//*[@id=\"authcode\"]")
	inputElement.send_keys(sgCode)
	time.sleep(1)

	"""Click on the submit button to login on Steam Guard email code."""
        driver.find_element_by_xpath("//*[@id=\"auth_buttonset_entercode\"]/div[1]").click()
        time.sleep(1)

        """Click the button to confirm the success of the Steam Guard code sent to the email."""
        driver.find_element_by_xpath("//*[@id=\"success_continue_btn\"]").click()
        time.sleep(3)

"""Condition to redirect to the key activation page after login is done."""
if driver.current_url == "http://store.steampowered.com/":
    driver.get("https://store.steampowered.com/account/registerkey")

"""Click on the acceptance box for the terms of the service."""
driver.find_element_by_xpath("//*[@id=\"accept_ssa\"]").click()
time.sleep(1)

"""Cycle to read the keys of a file and activate one by one in the Steam."""
ref_arquivo = open("keys.txt","r")
linha = ref_arquivo.readline()
while linha:
    """Select the key text input."""
    inputElement = driver.find_element_by_xpath("//*[@id=\"product_key\"]")
    inputElement.send_keys(linha)
    time.sleep(1)

    """Click on the button to activate the key."""
    driver.find_element_by_xpath("//*[@id=\"register_btn\"]").click()
    time.sleep(3)

    """Condition to check if an error occurred activating the key."""
    if driver.find_element_by_xpath("//*[@id=\"error_display\"]").is_displayed():
        print("Already have the game or the key is invalid: " + linha)

        """Clears the textbox where the keys are placed."""
        driver.find_element_by_xpath("//*[@id=\"product_key\"]").clear()
        time.sleep(1)

    else:
        print("The game was successfully activated.: " + linha)
        
        """Click on the button to return to the activate keys page."""
        driver.find_element_by_xpath("//*[@id=\"receipt_form\"]/div[3]/a[1]").click()
        time.sleep(3)

        """Click on the acceptance box for the terms of the service."""
        driver.find_element_by_xpath("//*[@id=\"accept_ssa\"]").click()
        time.sleep(1)
        
    
    linha = ref_arquivo.readline()
    
ref_arquivo.close()

driver.close()
