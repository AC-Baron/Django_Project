from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Recipe, Comment
from django.conf import settings
from .forms import RecipeForm
from .forms import RecipeForm, IngredientFormSet
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient
from .forms import RecipeForm, IngredientForm



# Homepage view
def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {'recipes': recipes})


# Recipe list view
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes})


# Recipe detail view
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.all().order_by('-created_on')

    # Handle comment submission
    if request.method == "POST":
        if request.user.is_authenticated:
            text = request.POST.get("text")
            if text.strip():
                Comment.objects.create(recipe=recipe, user=request.user, text=text)
                return redirect('recipe_detail', pk=pk)
        else:
            return redirect('login')

    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'comments': comments,
    })


# Toggle Favorite
@login_required
def toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    user = request.user

    if user in recipe.favorited_by.all():
        recipe.favorited_by.remove(user)
    else:
        recipe.favorited_by.add(user)

    return redirect('recipe_detail', pk=pk)


# ✅ Updated Cookbook View
@login_required
def cookbook(request):
    user = request.user

    # Recipes created by the current user
    my_recipes = Recipe.objects.filter(author=user)

    # Recipes the user has favorited
    favorite_recipes = user.favorite_recipes.all()

    return render(request, 'cookbook.html', {
        'my_recipes': my_recipes,
        'favorite_recipes': favorite_recipes,
    })


# Account page
@login_required
def account(request):
    return render(request, 'account.html')


# Edit comment
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if not (request.user == comment.user or request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You don't have permission to edit this comment.")
        return redirect('recipe_detail', pk=comment.recipe.pk)

    if request.method == "POST":
        new_text = request.POST.get("text")
        if new_text.strip():
            comment.text = new_text
            comment.save()
            messages.success(request, "Comment updated successfully!")
            return redirect('recipe_detail', pk=comment.recipe.pk)

    return render(request, 'edit_comment.html', {'comment': comment})


# Delete comment
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if not (request.user == comment.user or request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You don't have permission to delete this comment.")
        return redirect('recipe_detail', pk=comment.recipe.pk)

    recipe_id = comment.recipe.pk
    comment.delete()
    messages.success(request, "Comment deleted successfully!")
    return redirect('recipe_detail', pk=recipe_id)

# Create recipe view
@login_required
def create_recipe(request):

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        formset = IngredientFormSet(request.POST, prefix='ingredients')

        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            formset.instance = recipe
            formset.save()
            messages.success(request, "Recipe created successfully!")
            return redirect('recipe_detail', pk=recipe.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RecipeForm()
        formset = IngredientFormSet(prefix='ingredients')

    return render(request, 'create_recipe.html', {
        'form': form,
        'formset': formset
    })

# Edit recipe view
@login_required
def edit_recipe(request, pk):
    # Allow owner OR admin to edit the recipe
    if request.user.is_staff or request.user.is_superuser:
        recipe = get_object_or_404(Recipe, pk=pk)
    else:
        recipe = get_object_or_404(Recipe, pk=pk, author=request.user)

    IngredientFormSet = inlineformset_factory(
        Recipe,
        Ingredient,
        form=IngredientForm,
        extra=0,
        can_delete=True
    )

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = IngredientFormSet(request.POST, instance=recipe, prefix='ingredients')

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Recipe updated successfully!")
            return redirect('recipe_detail', pk=recipe.pk)

    else:
        form = RecipeForm(instance=recipe)
        formset = IngredientFormSet(instance=recipe, prefix='ingredients')

    return render(request, 'edit_recipe.html', {
        'form': form,
        'formset': formset,
        'recipe': recipe
    })

#delete recipe view
@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)

    if request.method == "POST":
        recipe.delete()
        return redirect('cookbook')  # redirect wherever you want after deletion

    return render(request, "delete_recipe_confirm.html", {"recipe": recipe})