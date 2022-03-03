from django.urls import path

from .views import index, register, login, app, db

urlpatterns = [
    path('', index, name='index'),
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('app', app, name='app'),
    path('db', db, name='database')
]
