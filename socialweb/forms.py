from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from socialweb.models import UserProfileModel,PostModel


class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput())
    password=forms.CharField(widget=forms.PasswordInput())

class ProfileAddForm(forms.ModelForm):
    class Meta:
        model=UserProfileModel
        fields=["profile_pic","bio","time_line_pic"]

class PostAddForm(forms.ModelForm):
    class Meta:
        model=PostModel
        fields=["caption","image"]





