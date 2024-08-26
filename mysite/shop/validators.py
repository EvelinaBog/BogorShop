from django.core.exceptions import ValidationError
from PIL import Image


def validate_image_size(image):
    with Image.open(image) as img:
        width, height = img.size
        if width > 70 or height > 70:
            raise ValidationError('Image dimensions should not exceed 70x70 pixels.')


def validate_image_upload_size(image):
    with Image.open(image) as img:
        width, height = img.size
        if width > 900 or height > 900:
            raise ValidationError('Image dimensions should not exceed 900x900 pixels.')

