from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.User_Add.as_view(),name="main ")
    ]