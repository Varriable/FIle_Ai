from django import forms
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['name', 'file']

class AskForm(forms.Form):
    prompt = forms.CharField(label='Ask something', required=False)
