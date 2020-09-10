from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import HttpResponseRedirect, render, reverse

from recipe.forms import AddAuthorForm, AddRecipeForm, LoginForm
from recipe.models import Author, Recipe, Favorite


# Create your views here.
def index(request):
    my_recipes = Recipe.objects.all()
    return render(request, "index.html", {"recipe_box": "My Recipe Box", "recipes": my_recipes})


def author_detail(request, author_id):
    the_author = Author.objects.filter(id=author_id).first()
    recipe_contributed = Recipe.objects.filter(author=the_author)
    return render(request, "author_detail.html", {"author": the_author, "recipes": recipe_contributed})


def recipe_detail(request, recipe_id):
    the_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {"recipe": the_recipe})


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user.author
        new_recipe.save()
        return HttpResponseRedirect(reverse("home"))
    form = AddRecipeForm()
    return render(request, "generic_view.html", {"form": form})


@login_required
def edit_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    if request.method == "POST":
        form = AddRecipeForm(request.POST, instance=recipe)
        form.save()
        return HttpResponseRedirect(reverse("recipe", args=[recipe.id]))

    form = AddRecipeForm(instance=recipe)
    return render(request, "generic_view.html", {"form": form})


def favorite_view(request, author_id):
    author = Author.objects.get(id=author_id)
    favorites = Favorite.objects.filter(author=author)
    return render(request, "favorites.html", {"favorites": favorites, "author": author.name})


@login_required
def add_favorite_recipe(request, recipe_id):
    if Favorite.objects.filter(author=Author.objects.get(user=request.user), recipe=Recipe.objects.get(id=recipe_id)):
        return HttpResponseRedirect(reverse("recipe", args=[recipe_id]))
    else:
        Favorite.objects.create(
            author=Author.objects.get(user=request.user),
            recipe=Recipe.objects.get(id=recipe_id),
        )
    return HttpResponseRedirect(reverse("recipe", args=[recipe_id]))


@login_required
def add_author(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = AddAuthorForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_user = User.objects.create_user(username=data.get("username"), password=data.get("password"))
                Author.objects.create(
                    name=data.get("name"),
                    bio=data.get("bio"),
                    user = new_user
                )
            return HttpResponseRedirect(reverse("home"))
    else:
        return HttpResponseForbidden("No, you can't do that...")
    form = AddAuthorForm()
    return render(request, "generic_view.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form =LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get("username"), password=data.get("password"))
            if user:
                login(request, user)
            return HttpResponseRedirect(request.GET.get("next", reverse("home")))
    form = LoginForm()
    return render(request, "generic_view.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))
