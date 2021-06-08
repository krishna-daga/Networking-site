from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass
class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=500, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User,  blank=True, related_name="liked_user")
    def __str__(self):
        return self.user.username



    
