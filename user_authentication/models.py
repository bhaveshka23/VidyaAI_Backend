from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lang = models.TextField()
    education = models.CharField(max_length=30)
    age = models.IntegerField()
    grade = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
