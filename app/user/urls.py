from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name="index"),
    path('register/',register,name="register"),
    path('user/',dashboard_user_view,name="user"),
    path('logout/',logout_view,name="logout"),
    path('edit_user/', update_view, name="edit"),
    path('delete_instagram/<id>/',delete_instagram, name="delete_instagram"),

    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        activate, name='activate'),
]
