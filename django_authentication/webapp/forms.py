from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm


class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'username': 'User Name' , 'first_name':'First Name','last_name':'Last Name','email':'Email'}


class EditUserProfile(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email','date_joined','last_login']
        labels = {'username': 'User Name' , 'first_name':'First Name','last_name':'Last Name','email':'Email', 'date_joined':'Date Joined','last_login':'Last Login'}



class EditAdminProfile(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = '__all__'
        labels = {'username': 'User Name' , 'first_name':'First Name','last_name':'Last Name','email':'Email', 'date_joined':'Date Joined','last_login':'Last Login'}

