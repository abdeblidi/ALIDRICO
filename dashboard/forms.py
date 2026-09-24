from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control-custom',
            'placeholder': 'اسم المستخدم',
            'autofocus': True
        }),
        label='اسم المستخدم'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control-custom',
            'placeholder': 'كلمة المرور'
        }),
        label='كلمة المرور'
    )