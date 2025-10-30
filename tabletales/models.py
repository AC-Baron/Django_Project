from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.title