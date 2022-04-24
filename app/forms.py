from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField, PasswordChangeForm, AdminPasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput(attrs={'class':'form-input', 'placeholder':'New Password'}))

    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-input', 'placeholder':'Confirm Password'}))

    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-input', 'placeholder':'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'email': 'Email'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-input', 'placeholder':'Username'})
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class':'form-input', 'placeholder':'Username'}))
    
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-input', 'placeholder':'Password'}))

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old password"), strip=False, widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'class':'form-input', 'placeholder':'Current Password'}))

    new_password1 = forms.CharField(label=_("New password"), strip=False, widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-input', 'placeholder':'New Password'}), help_text=password_validation.password_validators_help_text_html())
    
    new_password2 = forms.CharField(label=_("Confirm New password"), strip=False, widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-input', 'placeholder':'Confirm New Password'}))


class MyPasswordResetForm(PasswordResetForm):
  email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={"autocomplete": "email", 'class':'form-input', 'placeholder':'Enter your Email'}))
  

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-input', 'placeholder':'New Password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-input', 'placeholder':'Confirm Password'}),
    )

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Customer Name'}),
            'locality': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Locality'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City'}),
            'state': forms.Select(attrs={'class': 'form-input', 'placeholder': 'State'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Zipcode'}),
        }