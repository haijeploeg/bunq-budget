from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from dashboard.models import Settings, MonetaryAccounts, ENVIRONMENT_CHOICES


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autofocus": "autofocus",
                "required": "required",
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "required": "required",
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autofocus": "autofocus",
                "required": "required",
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "required": "required",
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "required": "required",
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "required": "required",
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "required": "required",
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "required": "required",
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "required": "required",
            }
        ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class SettingsForm(forms.ModelForm):
    bunq_api_key = forms.CharField(
        max_length=64,
        min_length=64,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "pattern": ".{64}",
            }
        ))
    bunq_api_environment = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }),
        choices=ENVIRONMENT_CHOICES
    )

    class Meta:
        model = Settings
        fields = ('bunq_api_key', 'bunq_api_environment')


class MonetarySettings(forms.ModelForm):
    active = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "custom-switch-input"
            }),
        required=False,
        label=''
    )

    class Meta:
        model = MonetaryAccounts
        fields = ('active',)
