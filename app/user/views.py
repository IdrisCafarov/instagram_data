from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.conf import settings
# from account
#Selenium
from core.selenium_utils import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains



# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('user')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False

            user.save()
            current_site = get_current_site(request)
            print(current_site)
            mail_subject = 'Hesab aktivləşdirilməsi'
            ctx = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
            message = get_template('account_activate.html').render(ctx)
            to_email = form.cleaned_data.get('email')
            to_list = [to_email]
            from_mail = settings.EMAIL_HOST_USER
            msg = EmailMessage(mail_subject, message, from_mail, to_list)
            msg.content_subtype = 'html'
            msg.mixed_subtype = 'related'

            msg.send()
            messages.success(request,
                             'Uğurla qeydiyyatdan keçdiniz!Xahiş edirik mailinizə gələn mesajı təsdiq edəsiniz!')
            return redirect('/')
    else:
        form = RegisterForm()







    context['form'] = form
    return render(request, 'register.html', context)



def activate(request, uidb64, token):
    if request.user.is_authenticated:
        logout(request)
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect("/")
    else:
        return HttpResponse('Activation link is invalid!')

def index(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('user')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            login(request, user)

            return redirect('index')

    else:
        form = LoginForm()
    context["form"] = form
    return render(request, 'index.html', context)



def dashboard_user_view(request):
    context = {}

    user = get_object_or_404(MyUser, id=request.user.id)



    context['user'] = user

    return render(request, "user_profile.html",context)




def update_view(request):
    context = {}

    usr = get_object_or_404(MyUser, id=request.user.id)

    if request.method == 'POST' and 'sub_main' in request.POST:
        form = UpdateForm(request.POST, request.FILES or None, instance=usr)
        print("qaqaaaaa")
        if form.is_valid():

            print("qaqam zor")

            form.save()
            messages.success(request, 'Sizin məlumatlarınız uğurla yeniləndi!')

            return redirect('edit')
    else:
        form = UpdateForm(instance=usr)


    if request.method == 'POST' and 'modal_sub' in request.POST:
        form_modal = InstagramForm(request.POST)

        if form_modal.is_valid():
            login = request.POST['login']
            password = request.POST['password']

            instagram = form_modal.save(commit=False)
            instagram.user = usr


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

                messages.error(request, "Login səhifəsinin yükləmməsi uzun çəkdi. Zəhmət olmasa sonra yenidən cəhd edin.")
                print("Login page timeout.")
                driver.quit()
                return redirect('edit')

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
                        messages.error(request, "İntagram dataları alına bilmədi")
                    else:
                        instagram.follower = follower_count
                        instagram.follow = following_count
                        image_content = download_image(profile_picture_url)
                        if image_content:
                            # Save the image to the ImageField of the instance
                            file_name = f"{login}_profile_picture.jpg"
                            instagram.image.save(file_name, image_content, save=True)
                        instagram.save()
                    messages.success(request, "Uğurla instagram hesabını əlavə etdiz")





                else:
                    messages.error(request, "İntagram dataları alına bilmədi")
                    print("Login failed.")
            except TimeoutException:
                messages.error(request, "Login səhifəsinin yükləmməsi uzun çəkdi. Zəhmət olmasa sonra yenidən cəhd edin.")
                print("Login timeout.")
            except:
                messages.error(request, "Hesabınıza daxil olunmadı.")
                print("Login failed.")

            driver.quit()
    else:
        form_modal = InstagramForm()



    context['form'] = form
    context['user'] = usr
    context['form_modal'] = form_modal


    return render(request,"edit_user.html",context)


def delete_instagram(request,id):
    object = get_object_or_404(Instagram,id=id)
    object.delete()
    messages.success(request, 'Siz uğurla hesabı sildiz!')

    return redirect('edit')











