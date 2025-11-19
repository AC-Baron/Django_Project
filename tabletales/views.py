from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Recipe, Comment, Ingredient, Notification
from .forms import RecipeForm, IngredientForm, IngredientFormSet
from django.forms import inlineformset_factory
from django.contrib.auth import login
from .forms import SignUpForm


#Signup view
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipe_list')
    else:
        form = SignUpForm()

    return render(request, "signup.html", {'form': form})

# Homepage view
def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {'recipes': recipes})


# Recipe list view
def recipe_list(request):
    recipes = Recipe.objects.all()

    # Store the navigation origin
    request.session["back_url"] = request.path

    return render(request, 'recipe_list.html', {'recipes': recipes})



def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.all().order_by('-created_on')

    # Get stored back URL (from recipe_list or cookbook)
    back_url = request.session.get("back_url", reverse("recipe_list"))

    # Handle comment submission
    if request.method == "POST":
        if request.user.is_authenticated:
            text = request.POST.get("text")
            if text.strip():
                comment = Comment.objects.create(recipe=recipe, user=request.user, text=text)

                # Notify recipe owner (but not if owner comments on their own recipe)
                if recipe.author != request.user:
                    Notification.objects.create(
                        user=recipe.author,
                        message=f"{request.user.username} commented on your recipe '{recipe.title}'.",
                        link=reverse("recipe_detail", args=[recipe.pk])
                    )

            return redirect('recipe_detail', pk=pk)
        else:
            return redirect('login')

    return render(request, "recipe_detail.html", {
        "recipe": recipe,
        "comments": comments,
        "back_url": back_url,
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

        # If someone else favorites your recipe → notify the author
        if recipe.author != user:
            Notification.objects.create(
                user=recipe.author,
                message=f"{user.username} favorited your recipe '{recipe.title}'.",
                link=reverse("recipe_detail", args=[recipe.pk])
            )

    return redirect('recipe_detail', pk=pk)


# Cookbook View
def cookbook(request):
    user = request.user

    if user.is_authenticated:
        # Normal behaviour for logged-in users
        my_recipes = Recipe.objects.filter(author=user)
        favorite_recipes = user.favorite_recipes.all()
    else:
        # Prevent errors when user is not logged in
        my_recipes = []
        favorite_recipes = []
        messages.info(request, "You must be logged in to use this feature.")

    # Store back URL so detail pages work correctly
    request.session["back_url"] = request.path

    return render(request, 'cookbook.html', {
        'my_recipes': my_recipes,
        'favorite_recipes': favorite_recipes,
    })


# Account page
@login_required
def account(request):
    return render(request, 'account.html')


# Edit comment — inline on recipe page
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Permission check (owner or admin)
    if not (request.user == comment.user or request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You don't have permission to edit this comment.")
        return redirect('recipe_detail', pk=comment.recipe.pk)

    if request.method == "POST":
        new_text = request.POST.get("text", "").strip()
        if new_text:
            comment.text = new_text
            comment.save()
            messages.success(request, "Comment updated successfully!")
        return redirect('recipe_detail', pk=comment.recipe.pk)

    # If GET, place recipe page into edit mode
    return redirect(f"/recipe/{comment.recipe.pk}/?edit_comment={comment.id}")


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


# Create recipe
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


# Edit Recipe View
@login_required
def edit_recipe(request, pk):

    # Save where the user came FROM before editing
    from_url = request.GET.get("from")
    if from_url:
        request.session["back_url"] = from_url

    # Allow owner OR admin
    if request.user.is_staff or request.user.is_superuser:
        recipe = get_object_or_404(Recipe, pk=pk)
    else:
        recipe = get_object_or_404(Recipe, pk=pk, author=request.user)

    IngredientFormSet = inlineformset_factory(
        Recipe, Ingredient,
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

            # Notify recipe owner only if the editor is not the owner
            if recipe.author != request.user:
                Notification.objects.create(
                    user=recipe.author,
                    message=f"An admin updated your recipe '{recipe.title}'.",
                    link=reverse("recipe_detail", args=[recipe.pk])
                )

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


# Delete recipe
@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # Permission check: owner OR admin OR superuser
    if not (request.user == recipe.author or request.user.is_staff or request.user.is_superuser):
        raise Http404("You do not have permission to delete this recipe.")

    # Determine where to go AFTER deleting
    back_url = request.GET.get("from") or request.session.get("back_url") or reverse('cookbook')

    if request.method == "POST":

        # Notify the owner
        if recipe.author != request.user:
            Notification.objects.create(
                user=recipe.author,
                message=f"An admin deleted your recipe '{recipe.title}'.",
                link=""
            )
        recipe.delete()
        return redirect(back_url)

    return render(request, "delete_recipe_confirm.html", {
        "recipe": recipe,
        "back_url": back_url,
    })

#notifications
@login_required
def notifications_page(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # Mark all unread notifications as read
    notifications.filter(read=False).update(read=True)

    return render(request, 'notifications.html', {
        'notifications': notifications
    })
