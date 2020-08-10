from django import forms
from recipe.models import Author, Recipe


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "time_required", "instructions", "author"]

class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "bio"]