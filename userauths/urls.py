from django.urls import path
from .views import *

urlpatterns = [
    path("sign-up/", RegisterView, name="sign-up"),
    path("sign-in/", loginView, name="sign-in"),
    path("sign-out/", logoutView, name="sign-out"),
]