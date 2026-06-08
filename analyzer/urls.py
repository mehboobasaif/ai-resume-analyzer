from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('history/', views.history),
    path('register/', views.register),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
]