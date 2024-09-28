from django import forms
from .models import UploadedImage, Products

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['title', 'image']

