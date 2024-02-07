from typing import Any
from datetime import timedelta
from django import forms
from users.models import Person
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm
# from django.forms import 
from django.core.mail import send_mail
from users.models import EmailVerification
from django.utils.timezone import now

class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':'Введите имя'
        }
    ),label=False)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'placeholder':'mail@gmail.com'
        }
    ),label=False)
    class Meta:
        model = Person
        fields = ['username','email']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':'Введите имя'
        }
    ),label=False)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder':'Супер пароль'
        }
    ),label=False)
    class Meta:
        model = Person
        
#         fields = ['username','password']
        
class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':'Андрей'
        }
    ),label=False)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'placeholder':'mail@gmail.com'
        }
    ),label=False)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder':'Супер пароль'
        }
    ),label=False)
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder':'Повтор Супер пароля'
        }
    ),label=False)
    
    class Meta:
        model = Person
        fields = ['username','email','password1','password2']
        

    def save(self, commit: bool = True):
        user = super().save(commit)
        expiration = now() + timedelta(hours=24)
        record = EmailVerification.objects.create(
            code=user.id,
            user=user,
            expiration=expiration
        )
        record.send_verification_mail()
        return user

class UserSetPasswordForm(SetPasswordForm):

    class Meta:
        model = Person
