from django.urls import path
from .views import *

from . import views

urlpatterns = [
    path("register", RegisterAPIView.as_view(), name="register"),
    path("login", LoginAPIView.as_view(), name="login"),
    path("user", AuthUserAPIView.as_view(), name="auth-user"),
]
