from django.urls import path
from . import views

urlpatterns = [
    path('assistant', views.assistant, name = 'assistant'),
    path('', views.register, name = 'register'),
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('usersettings', views.usersettings, name = 'usersettings'),
]