
from django import forms

class UserLogin(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(), label='Email')
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput())
