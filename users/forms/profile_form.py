from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2'
            }),
        }

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']
        widgets = {
            'profile_image': forms.FileInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2'
            }),
        }