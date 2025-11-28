from django import forms
from myapp.models import *
from django.contrib.auth.hashers import make_password, check_password

class myupdateform(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    username = forms.CharField(
        label='username',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': True
        })
    )
    phone_number = forms.CharField(
        label='Contact Number',
        max_length=15,
        required=False,  
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your contact number'
        })
    )

# class ChangePasswordForm(forms.Form):
#     new_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'placeholder': 'Enter new password',
#             'class': 'form-control'
#         }),
#         label="New Password",
#         min_length=8,
#         max_length=128,
#         required=True
#     )
#     confirm_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'placeholder': 'Re-enter new password',
#             'class': 'form-control'
#         }),
#         label="Confirm Password",
#         min_length=8,
#         max_length=128,
#         required=True
#     )

#     def save(self):
#         old=super().save(commit=False)
#         old.password=make_password(self.cleaned_data['password'], hasher='argon2')
#         old.save()
#         return old

