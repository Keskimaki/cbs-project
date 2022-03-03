from django.http import HttpResponse
from django.shortcuts import redirect, render
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
        username = body['username']
        user = User.objects.get(username=username)

        if not user or body['password'] != body['password']:
            return render(request, 'pages/login.html')

        users = [ user.username for user in User.objects.all() ]
        messages = [ message.content for message in Message.objects.filter(receiver=user) ]

        context = {
            'username': username,
            'users': users,
            'messages': messages
        }

        return app(request, context)

    return render(request, 'pages/login.html')

def app(request, context=None):
    if context:
        return render(request, 'pages/app.html', context)

    if request.method == 'POST':
        body = request.POST
        receiver = User.objects.get(username=body['receiver'])

        message = Message(id=id_generator(False), content=body['content'], receiver=receiver)
        message.save()

        return redirect('/')

def db(request):
    users = [ f'{user.username};{user.password}' for user in User.objects.all() ]
    messages = [ f'{message.content};{message.receiver.username}' for message in Message.objects.all() ]

    data = ""

    for user in users:
        data += user + '\n'
    data += '\n\n'
    for message in messages:
        data += message + '\n'    

    return HttpResponse(data)

def id_generator(user=True):
    if user:
        id = User.objects.latest('id').id
    else:
        id = Message.objects.latest('id').id

    id += 1

    return id
