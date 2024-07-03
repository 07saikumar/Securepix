from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django import forms
from .models import UploadedImage
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        # Check for minimum length
        if len(password1) < 8:
            raise forms.ValidationError('The password must be at least 8 characters long.')
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password1):
            raise forms.ValidationError('The password must contain at least one uppercase letter.')
        
        # Check for alphanumeric requirement (both letters and numbers)
        if not re.search(r'[a-zA-Z]', password1) or not re.search(r'\d', password1):
            raise forms.ValidationError('The password must be alphanumeric (contain both letters and numbers).')
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise forms.ValidationError('The password must contain at least one special character.')

        return password1

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']
