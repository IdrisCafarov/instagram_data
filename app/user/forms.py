from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from account.models import *


# get custom user
User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={
        'type':'email',
        'class':'form-control ',
        'placeholder':'Email',
        }
    ))
    name=forms.CharField(max_length=1200,widget=forms.TextInput(attrs={
        'type':'text',
    	'class':'form-control',
    	'placeholder':'Ad',
        'autofocus': '',
    	}))
    surname=forms.CharField(max_length=1200,widget=forms.TextInput(attrs={
        'type':'text',
        'class':'form-control',
        'placeholder':'Soyad'
        }))
    password1=forms.CharField(max_length=100,widget=forms.PasswordInput(
        attrs={
        'type':'password',
        'class':'form-control',
        'placeholder':'Şifrə'
        }
    ))
    password2=forms.CharField(max_length=100,widget=forms.PasswordInput(
        attrs={
        'type':'password',
        'class':'form-control',
        'placeholder':'Şifrəni doğrula'
        }
    ))


    class Meta:
        model = User
        fields = ('name','name','email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            match = MyUser.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Bu email artıq mövcuddur.Yenisini yoxlayın!')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""




class LoginForm(forms.Form):
    email= forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={
        'type':'email',
        'class':'form-control',
        'placeholder':'Enter your Email'
        }
    ))
    password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={
        'type':'password',
        'class':'form-control',
        'placeholder':'Enter your Password'
        }
    ))

    def clean(self):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        if email and password:
            user=authenticate(email=email,password=password)
            if not user or user.is_superuser==True:
                raise forms.ValidationError('Email və ya Şifrə yanlışdır !')




        return super(LoginForm, self).clean()



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""




class UpdateForm(forms.ModelForm):
    email= forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={
        'type':'email',
        'class':'form-control',
        'id':'email',
        'placeholder':'your@example.com',
        'readonly':True
        }
    ))





    name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={
        'type':'email',
        'class':'form-control',
        'id':'firstName',
        'placeholder':'Enter your First Name'

        }
    ))
    surname=forms.CharField(max_length=100,widget=forms.TextInput(attrs={
        'type':'email',
        'class':'form-control',
        'id':'lastName',
        'placeholder':'Enter your Last Name'
        }
    ))

    profil_image=forms.FileField(widget=forms.FileInput(attrs={
        'type':'file',
        'class':'form-file-input form-control',
        }
    ))


    class Meta:
        model = MyUser
        fields = ('name','surname','email','profil_image')




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""






class InstagramForm(forms.Form):

    login= forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'type':'text',
        'placeholder':'username',
        }
    ))
    password= forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'type':'password',
        'placeholder':'password'
        }
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
