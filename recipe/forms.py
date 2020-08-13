from django import forms
from recipe.models import Author, Recipe


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "time_required", "instructions"]


class AddAuthorForm(forms.ModelForm):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Author
        fields = ["name", "bio"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)

