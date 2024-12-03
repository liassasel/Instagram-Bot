from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time

load_dotenv()

USERNAME = os.getenv("USERNAMEE")
PASSWORD = os.getenv("PASSWORD")
MAX_TIME_LOAD = 20
MIN_TIME_LOAD = 2

xpath = {
    "decline_cookies": "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]",
    "save_login_not_now_button": "//div[contains(text(), 'Ahora no')]",
    "notification_not_now_button": "//button[contains(text(), 'Ahora no')]",
    "like_button": "//*[@aria-label='Me gusta']",
    "modal": "//div[@role='dialog']",
    "cancel_unfollow_button": "//button[contains(text(), 'Cancel')]",
    "followers_button": "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a",
    "follows_button": "/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div/div/div/div[3]/div/button"
}

css_selector = {
    "follows_buttons": "._aano button"
}

urls = {
    "login": "https://www.instagram.com/accounts/login/",
    "post": "https://www.instagram.com/p/CzZQt6BIsck/"
}


class InstaFollower:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def close_browser(self):
        self.driver.close()

    def login(self):
        self.driver.get(urls["login"])

        try:
            cookie_warning = WebDriverWait(self.driver, MIN_TIME_LOAD).until(
                EC.presence_of_element_located((By.XPATH, xpath["decline_cookies"]))
            )
            # Dismiss the cookie warning by clicking an element or button
            cookie_warning[0].click()
        except:
            pass 

        username = self.driver.find_element(by=By.NAME, value="username")
        password = self.driver.find_element(by=By.NAME, value="password")

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        WebDriverWait(self.driver, MIN_TIME_LOAD)
        password.send_keys(Keys.ENTER)

        try:
            # Click "Not now" and ignore Save-login info prompt
            save_login_prompt = WebDriverWait(self.driver, MIN_TIME_LOAD).until(
                EC.presence_of_element_located((By.XPATH, xpath["save_login_not_now_button"]))
            )
            save_login_prompt.click()
        except:
            pass

        try:
            # Click "not now" on notifications prompt
            notifications_prompt = WebDriverWait(self.driver, MIN_TIME_LOAD).until(
                EC.presence_of_element_located((By.XPATH, xpath["notification_not_now_button"]))
            )
            notifications_prompt.click()
        except:
            pass

    def like_to_post(self):
        self.driver.get(xpath["post"])

        # Click like
        like_button = WebDriverWait(self.driver, MAX_TIME_LOAD).until(
        EC.element_to_be_clickable((By.XPATH, xpath["like_button"]))
        )
        like_button.click()
        print("Like dado")
        
        # Acount navigate
    def find_account(self, account_name):
        print('Navegando al perfil')
        self.driver.get(f"https://www.instagram.com/{account_name}")
        time.sleep(4)

    def find_followers(self):
        print('Abriendo la lista de seguidores')
        try:
            followers_button = WebDriverWait(self.driver, MAX_TIME_LOAD).until(
                EC.element_to_be_clickable((By.XPATH, xpath["followers_button"]))
            )
            followers_button.click()
            time.sleep(4)

            modal = WebDriverWait(self.driver, MAX_TIME_LOAD).until(
                EC.presence_of_element_located((By.XPATH, xpath["modal"]))
            )
            print("Modal de seguidores encontrado")
            
            for _ in range(5):  # Reducido a 5 iteraciones para pruebas
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
                time.sleep(5)
        except TimeoutException:
            print("No se pudo cargar la lista de seguidores. Verifica el XPath del botón de seguidores y del modal.")
        except Exception as e:
            print(f"Error al cargar seguidores: {str(e)}")

    def follow(self):
        print("Iniciando proceso de seguimiento")
        try:
            buttons = WebDriverWait(self.driver, MAX_TIME_LOAD).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Seguir') and not(contains(., 'Siguiendo'))]"))
            )
            
            for button in buttons:
                try:
                    button.click()
                    time.sleep(5)
                    print("Usuario seguido")
                except ElementClickInterceptedException:
                    print("No se pudo hacer clic en el botón de seguir")
                except Exception as e:
                    print(f"Error al seguir: {str(e)}")
            
            print('Fin del proceso de seguimiento')
        except TimeoutException:
            print("No se encontraron botones de seguir o se agotó el tiempo de espera. Verifica el XPath de los botones de seguir.")
        except Exception as e:
            print(f"Error en el proceso de seguimiento: {str(e)}")
            
bot = InstaFollower()
bot.login()
bot.find_account('5amoljen')
bot.find_followers()
bot.follow()
bot.close_browser()