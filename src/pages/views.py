from django.shortcuts import render
from .models import User

def index(request):
    return render(request, 'pages/index.html')

def register(request):
    if request.method == 'POST':
        body = request.POST
        user = User(id_generator(), body['username'], body['password'])
        user.save()

    return render(request, 'pages/register.html')

def login(request):
    if request.method == 'POST':
        body = request.POST
        user = User.objects.get(username=body['username'])

        if not user or user.password != body['password']:
            return render(request, 'pages/login.html')

        print('logged in')

    return render(request, 'pages/login.html')

def id_generator():
    id = User.objects.latest('id').id
    id += 1
    return id
