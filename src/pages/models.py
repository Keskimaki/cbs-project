from django.db import models

class User(models.Model):
    username = models.TextField(unique=True)
    password = models.TextField()
    time = models.DateField(auto_now_add=True)

class Message(models.Model):
    content = models.TextField()
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateField(auto_now_add=True)
