from django import forms
from .models import Resume
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["file"]

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
