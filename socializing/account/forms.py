from django import forms
from django.forms import TextInput
from django.contrib.auth.models import User
from nocaptcha_recaptcha.fields import NoReCaptchaField
from .models import Profile
from django.forms.extras.widgets import SelectDateWidget


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    captcha = NoReCaptchaField()

    class Meta:
        model = User
        fields = ('username',)
        #exclude = ['last_login', 'is_superuser', 'groups', 'user_permissions', 'last_name', 'date_joined', 'is_staff', 'is_active']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    # birthdate = forms.DateField(widget=SelectDateWidget(years=range(1920, 2021)))

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'city', 'country', 'education', 'photo')
        widgets = {'date_of_birth': TextInput(attrs={'placeholder': "Year-Month-Day"})}


