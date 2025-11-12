from django import forms
from .models import Recipe, Ingredient

from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'image', 'instructions']

# Ingredient form
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']

# Inline formset: allows editing ingredients alongside the recipe
IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm,
    extra=3, can_delete=True
)
