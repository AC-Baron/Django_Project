from django import forms
from .models import Recipe, Ingredient
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput

class CloudinaryImageInput(ClearableFileInput):
    """Custom widget for Cloudinary images that handles URL display properly"""

    def render(self, name, value, attrs=None, renderer=None):
        # Get the rendered HTML from parent
        html = super().render(name, value, attrs, renderer)

        # If we have a value (existing image), add a preview
        if value and hasattr(value, 'url'):
            try:
                preview_html = f'<div style="margin-top: 10px;"><img src="{value.url}" style="max-width: 200px; max-height: 200px;" alt="Current image"><br><small>Current image preview</small></div>'
                html += preview_html
            except Exception:
                # If URL access fails, just show the file input without preview
                pass

        return html

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
        widgets = {
            'image': CloudinaryImageInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make image field not required for editing (optional)
        self.fields['image'].required = False

# Ingredient form
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']

# Inline formset: allows editing ingredients alongside the recipe
IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm,
    extra=1, can_delete=True
)
