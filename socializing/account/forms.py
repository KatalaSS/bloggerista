import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.extras import SelectDateWidget
from django.forms.widgets import PasswordInput, TextInput

from .models import Profile
from captcha.fields import ReCaptchaField

User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'span2', 'placeholder': 'username'}), label='')
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'span2', 'placeholder': 'password'}), label='')


class UserCreateForm(UserCreationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'span2', 'placeholder': 'username'}), label='')
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'span2', 'placeholder': 'password'}), label='')
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'span2', 'placeholder': 'confirm your password'}),
                                label='')
    captcha = ReCaptchaField(label='', attrs={'size': 'compact'})

    class Meta:
        model = User
        fields = ("username",)
        # fields = "__all__"


class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'span2', 'placeholder': 'username'}), label='Username',)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    present = datetime.datetime.now().year
    date_of_birth = forms.DateField(widget=SelectDateWidget(attrs={'style': 'width: 32.5%; display: inline-block;'},
                                                            years=range(1950, present)))

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'city', 'country', 'education', 'photo')
        # widgets = {'date_of_birth': TextInput(attrs={'placeholder': "Year-Month-Day"})}
