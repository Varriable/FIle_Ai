from django import forms
from .models import FileDocument

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileDocument
        fields = ['title', 'file']

class AnalysisQueryForm(forms.Form):
    query = forms.CharField(
        label='Ask a question about the document',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your question...'})
    )