# tabletales/models.py
from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    description = models.TextField(blank=True)  # optional short summary
    image = models.ImageField(upload_to='recipes/', default='recipes/default.png', blank=True, null=True)
    instructions = models.TextField(help_text="Enter each step on a new line")
    created_on = models.DateTimeField(auto_now_add=True)

    favorited_by = models.ManyToManyField(User, related_name='favorite_recipes', blank=True)

    def get_instruction_steps(self):
        return [step.strip() for step in self.instructions.split('\n') if step.strip()]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.quantity})"
