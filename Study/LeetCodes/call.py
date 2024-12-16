from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import logging
import pickle

def login_to_leetcode(username, password):
    driver.get("https://www.leetcode.com/accounts/login/")
    time.sleep(2)

    # Find username and password fields and input the credentials
    driver.find_element("id", "id_login").send_keys(username)
    driver.find_element("id", "id_password").send_keys(password)
    driver.find_element("id", "id_password").send_keys(Keys.RETURN)
    time.sleep(10)


username = "Buuu29"
password = "Targaryen4life!"

logging.basicConfig(filename='example.log', filemode='w', encoding='utf-8', level=logging.INFO)

driver = webdriver.Chrome()

login_to_leetcode(username, password)

pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
# Adds the cookie into current browser context
# driver.add_cookie({"name": "csrftoken", "value": "bar"})

# # Get cookie details with named cookie 'foo'
# print(driver.get_cookie("csrftoken"))

# import requests

# # headers = {
# #     'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
# # }

# with requests.Session() as session:
#     url = "https://leetcode.com/accounts/login/"
#     result = session.get(url)
#     print(result.status_code, "\n")
#     print(result.content)





driver.quit()