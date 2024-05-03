from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from sitepages.models import Profile


class UserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirmed password"}))
    
    class Meta:
        model = User
        fields = ["username", "email"]
        
