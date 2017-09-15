# botSteamKeysActivation
 The following repository contains the code of a bot for bulk activation of Steam keys. This bot was written in Python using the Selenium framework.

#Usage Notes
 When you execute the bot you will be asked to enter your username, your password and the Steam Guard code, and for the latter code you must follow the following steps.

 Steam Guard by mobile app:
 - Open the Steam application for the mobile phone, type in the command line of the bot the Steam Guard code, and close the mobile application before exhausting the lifetime of that code.
 Steam Guard by email
 - For those who receive the Steam Guard codes by email, just go to the Steam site and log in, when the window asks for the code, go to the email and write the code that was sent to you at the command line of the bot.
 
 After the login is done do not need to do anything else, just have the keys of the games you want to activate in a text file with the name "keys.txt". The file should only contain one key per line.

#Dependencies
 - Python 2.7
 - Selenium
 - Webdriver for Firefox (This in case they use the bot as it is, if they decide to change use the webdriver of the browser of their choice.)
 
#License
 MIT
 Made in Portugal
