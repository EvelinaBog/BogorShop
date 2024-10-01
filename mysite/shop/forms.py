from django import forms
from .models import UploadedImage, Products, Cart


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['title', 'image']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'cols': 40,
            }),
        }
