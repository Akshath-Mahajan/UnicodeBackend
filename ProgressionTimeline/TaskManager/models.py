from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
class List(models.Model):
    name=models.TextField(max_length=16)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username+":"+self.name+":"+str(self.id)
class Task(models.Model):
    _list = models.ForeignKey(List, on_delete=models.CASCADE)
    title = models.TextField(max_length=16)
    description = models.TextField(max_length=1024)
    deadline = models.DateTimeField(null=True, blank=True)
    complete = models.BooleanField(default=False)   #For todo list later
    date_complete = models.DateTimeField(null=True, blank=True, default=None)
    def __str__(self):
        return self._list.user.username+":"+self.title+":"+str(self.id)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

post_save.connect(create_token, sender=User)