from django import forms
from .models import UploadedImage, Products, Order


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['title', 'image']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['comment']
