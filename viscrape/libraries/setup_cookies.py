import json, time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver

def getCookiesGUI(exepath, driverpath, firstpage="https://www.google.com/"):
   options = Options()
   options.add_argument("--incognito")
   options.add_experimental_option("excludeSwitches", ["enable-logging"])
   options.binary_location = exepath

   driver = webdriver.Chrome(service=Service(executable_path=driverpath), options=options)

   driver.get(firstpage)

   cookies = None
   while True:
      try:
         cookies = driver.get_cookies()
         time.sleep(0.2)
      except Exception:
         break

   return cookies

def saveCookies(cookies, path="./cookies.json"):
   if (cookies is None): cookies = {}

   with open(f"{path}", "w") as cookiesJSON:
      json.dump(cookies, cookiesJSON)