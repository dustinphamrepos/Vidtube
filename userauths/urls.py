from django.urls import path
from .views import RegisterView

urlpatterns = [
    path("sign-up/", RegisterView, name="sign-up"),
]