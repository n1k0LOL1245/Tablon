from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Pin, Rating

MAX_MB = 50


class PinForm(forms.ModelForm):
    class Meta:
        model = Pin
        fields = ["title", "description", "media"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

    def clean_media(self):
        f = self.cleaned_data["media"]
        if f.size > MAX_MB * 1024 * 1024:
            raise forms.ValidationError(f"El archivo no puede superar {MAX_MB} MB.")
        return f


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["stars"]


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username"]
