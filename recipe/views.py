from django.shortcuts import render, HttpResponseRedirect, reverse
from recipe.models import Author, Recipe
from recipe.forms import AddRecipeForm, AddAuthorForm


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


def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get("title"),
                description=data.get("description"),
                instructions=data.get("instructions"),
                time_required=data.get("time_required"),
                author=data.get("author"),
            )
            return HttpResponseRedirect(reverse("home"))
    form = AddRecipeForm()
    return render(request, "generic_view.html", {"form": form})

def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data.get("name"),
                bio=data.get("bio")
            )
            return HttpResponseRedirect(reverse("home"))
    form = AddAuthorForm()
    return render(request, "generic_view.html", {"form": form})