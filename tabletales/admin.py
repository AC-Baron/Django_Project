from django.contrib import admin

# Register your models here.

from .models import Recipe, Ingredient


class IngredientInline(admin.TabularInline):  # or StackedInline for vertical layout
    model = Ingredient
    extra = 1  # show 1 empty ingredient row by default


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on')
    inlines = [IngredientInline]