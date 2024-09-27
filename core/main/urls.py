from django.urls import path
from .views import (
    ItemListAPIView,
    UserLoginAPIView,
    UserRegisterAPIView,
    UserLogoutAPIView,
)

urlpatterns = [
    path("item-list", ItemListAPIView.as_view(), name="item-list"),
    # Registration section of urls.py
    path("login", UserLoginAPIView.as_view(), name="user_login"),
    path("register", UserRegisterAPIView().as_view(), name="user_register"),
    path("logout", UserLogoutAPIView.as_view(), name="user_logout"),
]
