from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .models import Recipe, Comment
from django.conf import settings


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

@login_required #Toggle Favourite
def toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    user = request.user

    # If user already favorited → remove it, else → add it
    if user in recipe.favorited_by.all():
        recipe.favorited_by.remove(user)
    else:
        recipe.favorited_by.add(user)

    # Redirect back to recipe detail page
    return redirect('recipe_detail', pk=pk)

@login_required #Cookbook View
def cookbook(request):
    recipes = request.user.favorite_recipes.all()
    return render(request, 'cookbook.html', {'recipes': recipes})

@login_required
def account(request):
    return render(request, 'account.html')

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Only staff/superusers or the comment's author can edit
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


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Only staff/superusers or the comment's author can delete
    if not (request.user == comment.user or request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You don't have permission to delete this comment.")
        return redirect('recipe_detail', pk=comment.recipe.pk)

    recipe_id = comment.recipe.pk
    comment.delete()
    messages.success(request, "Comment deleted successfully!")
    return redirect('recipe_detail', pk=recipe_id)