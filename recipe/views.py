from django.shortcuts import render
from recipe.models import Author, Recipe

# Create your views here.
def index(request):
    my_recipes = Recipe.objects.all()
    return render(request, "index.html", {"recipe_box": "My Recipe Box", "recipes": my_recipes})


def  author_detail(request, author_id):
    the_author = Author.objects.filter(id=author_id).first()
    recipe_contributed = Recipe.objects.filter(author=the_author)
    return render(request, "author_detail.html", {"author": the_author, "recipes": recipe_contributed})


def recipe_detail(request, recipe_id):
    the_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {"recipe": the_recipe})
