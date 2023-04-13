from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings



# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self,email,password=None,is_active=True,is_staff=False,is_superuser=False, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None):
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(unique=True,max_length=120,null=True)
    name = models.CharField(max_length=40,verbose_name="İstifadəçi adı", blank=True, null=True)
    surname = models.CharField( max_length=40,verbose_name="İstifadəçi soyadı", blank=True, null=True)
    profil_image = models.ImageField(upload_to="Profile Image",null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True)


    timestamp = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.surname:
            return '%s %s'%(self.name,self.surname)
        return self.name

    def has_perm(self,perm,obj=None):
        return self.is_superuser

    def has_module_perms(self,app_label):
        return True

    def get_avatar(self):
        if self.profil_image:
            return self.profil_image.url
        else:
            return "/static/user_pp.png"


class Instagram(models.Model):
    login = models.CharField(max_length=40,unique=True,null=True)
    password = models.CharField(max_length=50)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE, related_name="instagram")
    follower = models.IntegerField(null=True,blank=True)
    follow = models.IntegerField(null=True,blank=True)
    image = models.ImageField(upload_to="instagram_pp",null=True)

    def __str__(self):
        return self.login


