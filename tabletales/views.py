from django.shortcuts import render

# Create your views here.
# Testing Index View
from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, World! This is the Tabletales homepage.")

from .models import Recipe
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {'recipes': recipes})