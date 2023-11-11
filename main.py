from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv("local.env")
DRIVER_PATH = "/Users/kajsa/Desktop/Development/chromedriver"
PROMISED_DOWN = float(os.getenv("PROMISED_DOWN"))
PROMISED_UP = float(os.getenv("PROMISED_UP"))
TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
TWITTER_PASS = os.getenv("TWITTER_PASS")


class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(service=Service(executable_path=driver_path))
        self.down = ""
        self.up = ""

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        sleep(1)
        self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        sleep(0.5)
        self.driver.find_element(By.CLASS_NAME, "js-start-test").click()
        sleep(40)
        self.driver.find_element(By.CLASS_NAME, "notification-dismiss").click()
        sleep(0.5)
        self.down = self.driver.find_element(By.CLASS_NAME, "download-speed").text
        self.up = self.driver.find_element(By.CLASS_NAME, "upload-speed").text
        if float(self.down) < PROMISED_DOWN or float(self.up) < PROMISED_UP:
            message = f"Hey @Eir. Why is my internet speed {self.down} down/{self.up} up when I pay for {PROMISED_DOWN} down/{PROMISED_UP} up?"
            self.tweet_at_provider(message)

    def tweet_at_provider(self, message):
        self.driver.get("https://twitter.com/")
        sleep(2)
        self.driver.find_element(By.XPATH,
                                 "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div[1]/a").click()
        sleep(3)
        username = self.driver.find_element(By.CSS_SELECTOR, "div input")
        username.send_keys("sapphiredream15")
        username.send_keys(Keys.ENTER)
        sleep(3)
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys("Cwd6yapjHekeZFS")
        password.send_keys(Keys.ENTER)
        sleep(4)
        self.driver.find_element(By.CLASS_NAME, "notranslate").send_keys(message)
        sleep(2)
        try:
            pop_up = self.driver.find_element(By.XPATH,
                                              "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div/div[2]/div[4]")
            pop_up.click()
            sleep(1)
        except NoSuchElementException:
            pass
        self.driver.find_element(By.XPATH,
                                 "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]").click()
        sleep(10)


twitter_bot = InternetSpeedTwitterBot(DRIVER_PATH)
twitter_bot.get_internet_speed()
