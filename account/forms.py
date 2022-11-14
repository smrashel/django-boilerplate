from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm
from django import forms
from .models import *


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'contact_number', 'employee_id', 'groups')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'contact_number', 'employee_id', 'groups', 'is_active')