# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from selenium import webdriver
from time import sleep

driver = webdriver.Chrome(executable_path= "C:/Users/Mathieu/.spyder-py3/chromedriver.exe")

driver.get("https://www.instagram.com/")
sleep(1)


#Suppress pop-up
pop_up = driver.find_element("xpath", "/html/body/div[4]/div/div/button[1]")
pop_up.click()


#Connect with good authentification
sleep(2)
username = ""  #to put
pwd = ""  #to put

User = driver.find_element("xpath", """//*[@id="loginForm"]/div/div[1]/div/label/input""")
User.send_keys(username)

password = driver.find_element("xpath", """//*[@id="loginForm"]/div/div[2]/div/label/input""")
password.send_keys(pwd)

sleep(1)
connect = driver.find_element("xpath", """//*[@id="loginForm"]/div/div[3]/button/div""")
connect.click()

#Do not save the authentification
sleep(7)
later = driver.find_element("xpath", "//button[contains(text(), 'Plus tard')]")
later.click()

#Do not authorize notifications
sleep(7)
notif = driver.find_element("xpath", "//button[contains(text(), 'Plus tard')]")
notif.click()

driver.get("https://www.instagram.com/matthieupvr/")
sleep(8)
followers = driver.find_element("xpath", "//button[contains(text(), 'followers')]")
followers.click()
