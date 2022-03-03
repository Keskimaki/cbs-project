from django.shortcuts import render
from .models import User, Message

def index(request):
    return render(request, 'pages/index.html')

def register(request):
    if request.method == 'POST':
        body = request.POST
        user = User(id=id_generator(), username=body['username'], password=body['password'])
        user.save()

    return render(request, 'pages/register.html')

def login(request):
    if request.method == 'POST':
        body = request.POST
        user = User.objects.get(username=body['username'])

        if not user or user.password != body['password']:
            return render(request, 'pages/login.html')

        return app(request, { 'username': body['username'] })

    return render(request, 'pages/login.html')

def app(request, user=None):
    if request.method == 'POST':
        body = request.POST
        receiver = User.objects.get(username=body['receiver'])
        print(receiver)

        message = Message(id=id_generator(False), content=body['content'], receiver=receiver)
        print(message)
        message.save()

        print(Message.objects.all())

    if not user:
        return render(request, 'pages/app.html', { 'username': 'Tester', 'users': [ user.username for user in User.objects.all() ] })

    return render(request, 'pages/app.html', user)

def id_generator(user=True):
    if user:
        id = User.objects.latest('id').id
    else:
        id = Message.objects.latest('id').id

    id += 1

    return id
