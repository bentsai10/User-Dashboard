from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('process_login', views.process_login),
    path('login', views.login),
    path('process_register', views.process_register),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('logout', views.logout)
]