from .custom_logger import logger
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, AdminPasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer


class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'First Name'}))

    last_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Last Name'}))

    password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'New Password'}))

    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Confirm Password'}))

    email = forms.CharField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-input', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']
        labels = {
            'email': 'Email'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})

    def clean_first_name(self):
        # Capitalize first letter of first name
        first_name = self.cleaned_data.get('first_name', '')
        return first_name.capitalize()

    def clean_last_name(self):
        # Capitalize first letter of last name
        last_name = self.cleaned_data.get('last_name', '')
        return last_name.capitalize()


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Username'}))

    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-input', 'placeholder': 'Password'}))


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old password"), strip=False, widget=forms.PasswordInput(
        attrs={"autocomplete": "current-password", 'class': 'form-input', 'placeholder': 'Current Password'}))

    new_password1 = forms.CharField(label=_("New password"), strip=False, widget=forms.PasswordInput(
        attrs={"autocomplete": "new-password", 'class': 'form-input', 'placeholder': 'New Password'}), help_text=password_validation.password_validators_help_text_html())

    new_password2 = forms.CharField(label=_("Confirm New password"), strip=False, widget=forms.PasswordInput(
        attrs={"autocomplete": "new-password", 'class': 'form-input', 'placeholder': 'Confirm New Password'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(
        attrs={"autocomplete": "email", 'class': 'form-input', 'placeholder': 'Enter your Email'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-input', 'placeholder': 'New Password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-input', 'placeholder': 'Confirm Password'}),
    )


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'locality_address',
                  'city', 'state', 'zipcode']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Customer Name'}),
            'phone': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Customer Phone Number'}),
            'locality_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City'}),
            'state': forms.Select(attrs={'class': 'form-input', 'placeholder': 'State'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Zipcode'}),
        }
