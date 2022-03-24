from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField, PasswordChangeForm, AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation

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


