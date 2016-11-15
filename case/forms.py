from django import forms
from django.contrib.auth.models import User

from .models import Case, Coordinate


class CaseForm(forms.ModelForm):

    class Meta:
        model = Case
        fields = ['watch_id', 'victim_name']


class CoordinateForm(forms.ModelForm):

    class Meta:
        model = Coordinate
        fields = ['latitude', 'longitude']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
