from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']