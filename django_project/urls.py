"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from tabletales import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('admin/', admin.site.urls),
    path('recipe/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('cookbook/', views.cookbook, name='cookbook'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('account/', views.account, name='account'),
    path('admin/', admin.site.urls),

    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    path('recipes/create/', views.create_recipe, name='create_recipe'),
    path('recipes/<int:pk>/edit/', views.edit_recipe, name='edit_recipe'),
    path("recipe/<int:pk>/delete/", views.delete_recipe, name="delete_recipe"),

    path("signup/", views.signup_view, name="signup"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)