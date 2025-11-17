from django import forms
from .models import Recipe, Ingredient
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Account Signup Form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Recipe form
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
