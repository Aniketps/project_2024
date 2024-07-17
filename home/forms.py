from django import forms

class AudioUploadForm(forms.Form):
    audio_file = forms.FileField()
    conversion_type = forms.CharField(widget=forms.HiddenInput(), required=False)
