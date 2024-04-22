from django import forms
from .models import MyUser


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['profile_picture']
