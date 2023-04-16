from celery import shared_task
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.shortcuts import get_object_or_404


from core.selenium_utils import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

import time
from account.models import *
from .celery import app

from django.core.mail import send_mail
from django.conf import settings


def update_instagram_data(login,password,instagram_id):
        instagram=Instagram.objects.get(id=instagram_id)


        driver = get_driver()


        driver.get("https://www.instagram.com/")

        if is_logged_in(driver):
            print("qaqa men girmisem e -1")
            # Click the profile icon to navigate to the profile page
            logout_url = "https://www.instagram.com/accounts/logout/"
            driver.get(logout_url)


        driver.get("https://www.instagram.com/accounts/login/")

        # Wait for the username input element to be present on the page

        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "username")))
        except TimeoutException:

            driver.quit()

        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(login)
        password_input.send_keys(password)

        time.sleep(2)
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        login_button.click()

        try:
            WebDriverWait(driver, 60).until(lambda d: d.execute_script("return /instagram.com\/accounts\/login/.test(window.location.href) == false"))

            if is_logged_in(driver):
                follower_count, following_count, profile_picture_url = get_instagram_data(driver, login)
                if follower_count is None or following_count is None or profile_picture_url is None:
                    print("Failed to get Instagram data")
                else:
                    instagram.follower = follower_count
                    instagram.follow = following_count
                    image_content = download_image(profile_picture_url)
                    if image_content:
                        # Save the image to the ImageField of the instance
                        file_name = f"{login}_profile_picture.jpg"
                        instagram.image.save(file_name, image_content, save=True)
                    instagram.save()






            else:
                print("Login failed.")
        except TimeoutException:
            print("Login timeout.")
        except:
            print("Login failed.")

        driver.quit()





@shared_task
def every_10():
    accounts = Instagram.objects.all()

    for account in accounts:
        update_instagram_data(account.login,account.password,account.id)


@shared_task
def update_instagram_data_task(login,password,id):

        user = get_object_or_404(MyUser, id=id)
        driver = get_driver()


        driver.get("https://www.instagram.com/")

        if is_logged_in(driver):

            print("qaqa men girmisem e -1")
            # Click the profile icon to navigate to the profile page
            logout_url = "https://www.instagram.com/accounts/logout/"
            driver.get(logout_url)


        driver.get("https://www.instagram.com/accounts/login/")


        # Wait for the username input element to be present on the page

        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "username")))
            data = True
        except TimeoutException:
            driver.quit()
            data = False
            return data

        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(login)
        password_input.send_keys(password)

        time.sleep(2)
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        login_button.click()

        try:
            print("burdayam da qaqa")
            WebDriverWait(driver, 60).until(lambda d: d.execute_script("return /instagram.com\/accounts\/login/.test(window.location.href) == false"))
            data =True


            if is_logged_in(driver):
                follower_count, following_count, profile_picture_url = get_instagram_data(driver, login)
                if follower_count is None or following_count is None or profile_picture_url is None:
                    send_mail(
                        'Notification',
                        'Failed to get Instagram data',
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=True,
                        )
                    print("Failed to get Instagram data")
                else:
                    instagram=Instagram.objects.create(user_id=id,login=login,password=password)
                    instagram.follower = follower_count
                    instagram.follow = following_count
                    image_content = download_image(profile_picture_url)
                    if image_content:
                        # Save the image to the ImageField of the instance
                        file_name = f"{login}_profile_picture.jpg"
                        instagram.image.save(file_name, image_content, save=True)
                    instagram.save()
                    send_mail(
                        'Notification',
                        'Successfully get data from instagram',
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=True,
                        )
                    print("Failed to get Instagram data")






            else:
                data = False
                send_mail(
                        'Notification',
                        'Login failed.',
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=True,
                        )
                print("Login failed.")
        except TimeoutException:
            data = False
            send_mail(
                        'Notification',
                        'Login timeout.',
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=True,
                        )
            print("Login timeout.")
        except:
            data = False
            send_mail(
                        'Notification',
                        'Login failed.',
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=True,
                        )
            print("Login failed.")

        driver.quit()

        return data


