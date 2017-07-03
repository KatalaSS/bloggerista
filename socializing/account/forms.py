from django import forms
from django.contrib.auth.models import User
from nocaptcha_recaptcha.fields import NoReCaptchaField
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'span2', 'placeholder': 'username'}), label='')
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'span2', 'placeholder': 'password'}), label='')


class UserCreateForm(UserCreationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'span2', 'placeholder': 'username'}), label='')
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'span2', 'placeholder': 'password'}), label='')
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'span2', 'placeholder': 'confirm your password'}),
                                label='')
    captcha = NoReCaptchaField(label='')

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "captcha")


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'city', 'country', 'education', 'photo')
        widgets = {'date_of_birth': TextInput(attrs={'placeholder': "Year-Month-Day"})}
