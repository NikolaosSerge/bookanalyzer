from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    """docstring for project."""

    title = models.CharField(max_length=100)
    contents = models.TextField(blank=True)
    upload = models.FileField(blank=True)
    data = models.TextField(blank=True)
    def __str__(self):
        return self.title
