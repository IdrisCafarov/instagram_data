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

