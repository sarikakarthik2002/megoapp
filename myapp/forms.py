from django import forms
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from cloudinary.forms import CloudinaryFileField

class coursesForm(forms.ModelForm):
    courseimg = CloudinaryFileField()
    class Meta:
        model=courses
        fields='__all__'
        widgets = {
            'corseconceptlist': forms.CheckboxSelectMultiple(), 
            'description':forms.Textarea(attrs={'rows':4,'cols':70}) 
        }
class courseconceptsform(forms.ModelForm):
    class Meta:
        model=courseconcepts
        fields='__all__'

class myregisterform(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['password', 'username', 'first_name', 'last_name', 'email', 'phone_number']
    
    def save(self):
        old=super().save(commit=False)
        old.password=make_password(self.cleaned_data['password'], hasher='argon2')
        old.save()
        return old

class myloginform(forms.Form):
    username=forms.CharField(max_length=20)
    password=forms.CharField(max_length=20,widget=forms.PasswordInput())

class adminusercreateform(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields='__all__'
    
    def save(self):
        old=super().save(commit=False)
        old.password=make_password(self.cleaned_data['password'], hasher='argon2')
        old.save()
        return old

class adminuserupdateform(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['username', 'first_name', 'last_name', 'email', 'phone_number', 'is_active', 'is_staff', 
              'is_superuser','address']
    
    