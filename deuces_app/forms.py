from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from deuces_app.models import Establishment
from deuces_app.models import Restroom
from deuces_app.models import Review


class DeucerForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "password" : forms.PasswordInput,
        }


class EstablishmentForm(ModelForm):
    class Meta:
        model = Establishment
        fields = ["name", "description"]


class RestroomForm(ModelForm):
    class Meta:
        model = Restroom
        fields = ["name", "description", "gender", "level", "features"]


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["review", "rating"]