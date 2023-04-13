from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from django.core.files.base import ContentFile


def is_logged_in(driver):
    try:
        WebDriverWait(driver, 30).until(lambda d: d.title.strip().lower() != "login • instagram")
        return True
    except TimeoutException:
        return False


def download_image(url):
    response = requests.get(url)

    if response.status_code == 200:
        return ContentFile(response.content)
    else:
        return None


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome_user_data")
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)
    return driver


def get_instagram_data(driver, username):
    try:
        # Navigate to the user's profile page
        profile_url = f"https://www.instagram.com/{username}/"
        driver.get(profile_url)

        # Get the follower count
        follower_count_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/followers/")]/span')))
        follower_count = int(follower_count_element.text.replace(',', ''))
        print(f"Follower count: {follower_count}")

        # Get the following count
        following_count_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/following/")]/span')))
        following_count = int(following_count_element.text.replace(',', ''))
        print(f"Following count: {following_count}")

        # Get the profile picture URL
        profile_picture_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "header img")))
        profile_picture_url = profile_picture_element.get_attribute("src")
        print(f"Profile picture URL: {profile_picture_url}")


        return follower_count, following_count, profile_picture_url

    except Exception as e:
        print(f"Error in get_instagram_data: {e}")
        return None, None, None
