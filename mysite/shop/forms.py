from django import forms
from .models import UploadedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['title', 'image']


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=0, max_value=100, label="Quantity")