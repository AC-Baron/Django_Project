# tabletales/models.py
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


def get_cloudinary_cloud_name():
    cloud_name = settings.CLOUDINARY_STORAGE.get('CLOUD_NAME') or os.environ.get('CLOUDINARY_CLOUD_NAME')
    if cloud_name:
        return cloud_name

    cloud_url = os.environ.get('CLOUDINARY_URL')
    if cloud_url and cloud_url.startswith('cloudinary://'):
        try:
            return cloud_url.split('@', 1)[1]
        except IndexError:
            return None
    return None


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    description = models.TextField(blank=True)  # optional short summary
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    instructions = models.TextField(help_text="Enter each step on a new line")
    created_on = models.DateTimeField(auto_now_add=True)

    favorited_by = models.ManyToManyField(User, related_name='favorite_recipes', blank=True)

    def get_instruction_steps(self):
        return [step.strip() for step in self.instructions.split('\n') if step.strip()]

    @property
    def image_url(self):
        if not self.image or not self.image.name:
            return None

        cloud_name = get_cloudinary_cloud_name()
        image_name = self.image.name.lstrip('/')

        if cloud_name:
            return f"https://res.cloudinary.com/{cloud_name}/image/upload/{image_name}"

        try:
            return self.image.url
        except Exception:
            return None

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

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.title}"
    
#Notification Model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)  # link to recipe page
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"