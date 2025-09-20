from django.db import models
from django.contrib.auth.models import User

class VisualAid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    question = models.CharField(max_length=1000)
    mermaid_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.question


