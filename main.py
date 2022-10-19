import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import sys
import urllib.parse

username = sys.argv[1]
password = sys.argv[2]
songs_list_path = sys.argv[3]
chromedriver_path = sys.argv[4]

songs_file = open(songs_list_path, 'r')
songs_file_lines = songs_file.readlines()


def create_chrome_options():
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    return chrome_options


driver = webdriver.Chrome(
    executable_path=chromedriver_path,
    options=create_chrome_options()
)
driver.implicitly_wait(10)

driver.get("https://accounts.spotify.com/en/login")
driver.find_element(By.ID, "login-username").send_keys(username)
driver.find_element(By.ID, "login-password").send_keys(password)
driver.find_element(By.ID, "login-button").click()
driver.find_element(By.XPATH, "//*[@data-testid='web-player-link']").click()

try:
    driver.find_element(By.XPATH, "//*[@data-testid='login-button']")
    exit()
except:
    print("Successfull login")

search_url = "https://open.spotify.com/search/"
i = 0
for l in songs_file_lines:
    i = i + 1
    print("Start processing song #{}".format(i))
    line = l.strip()
    print("Song: {}".format(line))
    search_path = urllib.parse.quote(line)
    driver.get(search_url + search_path)
    try:
        songs_element = driver.find_element(By.XPATH, "//section[@aria-label='Songs']")
    except:
        print("Can't find songs element")
        continue

    try:
        first_song = songs_element.find_element(By.XPATH, "(//div[@data-testid='tracklist-row'])[1]")
    except:
        print("Cant find first_song")
        continue

    try:
        like_button = first_song.find_element(By.XPATH, "//button[@aria-label='Save to Your Library']")
        like_button.click()
        print("Song was saved successfully: {}".format(line))
    except:
        print("Song is already in library {}".format(line))
        continue
driver.close()
