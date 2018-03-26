from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from deuces_app.models import Deucer

class DeucerForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "password" : forms.PasswordInput,
        }

