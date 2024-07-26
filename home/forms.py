from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import user_table

class AudioUploadForm(forms.Form):
    audio_file = forms.FileField()
    conversion_type = forms.CharField(widget=forms.HiddenInput(), required=False)

class user_login1(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class user_login(UserCreationForm):
    class Meta:
        model = user_table
        fields = ['first_name', 'last_name','email','username', 'password1', 'password2']