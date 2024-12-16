from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import logging

# Function to login to Instagram
def login_to_instagram(username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(2)

    # Find username and password fields and input the credentials
    driver.find_element("name", "username").send_keys(username)
    driver.find_element("name", "password").send_keys(password)
    driver.find_element("name", "password").send_keys(Keys.RETURN)
    time.sleep(10)

# Function to get list of likers
def get_likers(post_url):
    driver.get(post_url)

    time.sleep(5)

    # Click on the likes count to open the list of likers
    likes_element = driver.find_element("xpath", "//a[contains(@href, '/liked_by/')]")
    logging.info('we got the likes element')

    likes_element.click()
    logging.info('I guess we clicked the thing?')
    time.sleep(20)

    # Scroll through the list of likers to load all of them
    likers_popup = driver.find_element("xpath", "//div[@role='dialog']")
    likers_list = likers_popup.find_element("xpath", "//div[@class='PZuss']")
    prev_height = driver.execute_script("return arguments[0].scrollHeight;", likers_list)
    while True:
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", likers_list)
        time.sleep(2)
        new_height = driver.execute_script("return arguments[0].scrollHeight;", likers_list)
        if new_height == prev_height:
            break
        prev_height = new_height

    # Extract usernames of likers
    likers = likers_list.find_element("xpath", "//a[@class='FPmhX notranslate _0imsa ']")
    likers_names = [liker.text for liker in likers]

    return likers_names

# Provide your Instagram credentials here
username = "buuuu.29"
password = "Chessiscool123!"

logging.basicConfig(filename='example.log', filemode='w', encoding='utf-8', level=logging.INFO)

# Provide the URL of the post you want to get likers from
post_url = "https://www.instagram.com/p/C2reJVEq5AfR9ynmAj8E3wsKcGCHgFvgkd6mmg0/"

# Initialize Selenium webdriver
driver = webdriver.Chrome()

# Login to Instagram
login_to_instagram(username, password)

# Get list of likers
likers_list = get_likers(post_url)

# Print the list of likers
print("List of Likers:")
for liker in likers_list:
    print(liker)

# Close the webdriver
driver.quit()
