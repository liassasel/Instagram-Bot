from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import time
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

class InstaFollower:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        url = 'https://www.instagram.com/accounts/login/'
        self.driver.get(url)
        time.sleep(4)
        
        #Check if the cookie warning is present on te page
        decline_cookies_xpath = '"/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]'
        cookie_warning = self.driver.find_elements(By.XPATH, decline_cookies_xpath)
        if cookie_warning:
            # Demiss the cookie warning by clicking an element or button
            cookie_warning[0].click()
        
        username = self.driver.find_element(by=By.NAME, value='username')
        password = self.driver.find_elements(by=By.NAME, value='password')
        
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        
        time.sleep(2)
        password.send_key(Keys.ENTER)
        
        time.sleep(4)
        # Click 'Not now' and ignore Save-login inf
        save_login_prompt = self.driver.find_element(by=By.XPATH, value='// button[contains(text(), "Ahora no")]')
        if save_login_prompt:
            save_login_prompt.click()
            
        time.sleep(3)
        notifications_prompt = self.driver.find_element(by=By.XPATH, value='// button[contains(text(), "Ahora no")]')
        if notifications_prompt:
            notifications_prompt.click()

bot = InstaFollower()
bot.login()

