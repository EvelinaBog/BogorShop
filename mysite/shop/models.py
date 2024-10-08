from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator
from django.db import models
from .validators import validate_image_size
from io import BytesIO as io
from PIL import Image as PilImage
from .validators import validate_image_size, validate_image_upload_size
from PIL import Image
from django.contrib.auth.models import User
import datetime
import io
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your models here.


from PIL import Image as PilImage
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

def resize_image(image, size=(1080, 1080)):
    img = PilImage.open(image)
    original_size = img.size

    # Convert to RGB only if the image mode is not 'RGB' or 'RGBA'
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')

    img.thumbnail(size, PilImage.Resampling.LANCZOS)
    resized_size = img.size

    print(f"Original size: {original_size}, Resized size: {resized_size}")

    img_io = io.BytesIO()  # Corrected to use BytesIO
    img_format = 'PNG' if img.mode == 'RGBA' else 'JPEG'  # Preserve PNG for transparency

    # Save as PNG if it's RGBA, otherwise save as JPEG
    img.save(img_io, format=img_format, quality=85)  # Adjust quality for JPEG only

    img_io.seek(0)  # Rewind the file pointer

    # Create an InMemoryUploadedFile using the correct format
    img_file = InMemoryUploadedFile(
        img_io,
        'ImageField',
        image.name,
        f'image/{img_format.lower()}',  # Ensure the correct MIME type
        img_io.getbuffer().nbytes,
        None
    )

    print(f"File size after resize: {img_file.size} bytes")
    return img_file


class Products(models.Model):
    color = models.CharField(verbose_name='Color', max_length=20)
    remaining = models.FloatField(verbose_name='Remaining', default=0)
    price = models.FloatField(verbose_name='Price', default=1.99)
    image = models.ImageField(upload_to='flowers/')
    image_upload = models.ImageField(upload_to='bouquets/', blank=True, null=True)

    def __str__(self):
        return f'{self.color}'

    def update_remaining(self, roses_qty):
        self.remaining -= roses_qty
        return self.save()

    def save(self, *args, **kwargs):
        # Resize main image if it exceeds 70x70 pixels
        if self.image and hasattr(self.image, 'file'):
            self.image = resize_image(self.image, size=(70, 70))

        # Resize uploaded image if it exceeds 900x900 pixels
        if self.image_upload and hasattr(self.image_upload, 'file'):
            self.image_upload = resize_image(self.image_upload, size=(900, 900))

        # Save the instance
        super().save(*args, **kwargs)


class Decorations(models.Model):
    type = models.CharField(verbose_name='Type', max_length=20)
    remaining = models.FloatField(verbose_name='Remaining', default=0)
    price = models.FloatField(verbose_name='Price', default=0.49)
    deco_img = models.ImageField(upload_to='Decoration/')
    deco_img_upload = models.ImageField(upload_to='Decorations/', blank=True, null=True)

    def __str__(self):
        return f'{self.type}'

    def update_remaining(self, decoration_qty):
        self.remaining -= decoration_qty
        return self.save()

    def save(self, *args, **kwargs):
        # Resize main image if it exceeds 70x70 pixels
        if self.deco_img and hasattr(self.deco_img, 'file'):
            self.image = resize_image(self.deco_img, size=(70, 70))

        # Resize uploaded image if it exceeds 900x900 pixels
        if self.deco_img_upload and hasattr(self.deco_img_upload, 'file'):
            self.image_upload = resize_image(self.deco_img_upload, size=(900, 900))

        # Save the instance
        super().save(*args, **kwargs)


class WrappingPaper(models.Model):
    color = models.CharField(verbose_name='Color', max_length=20)
    remaining = models.FloatField(verbose_name='Remaining', default=0)
    price = models.FloatField(verbose_name='Price', default=0.25)

    def __str__(self):
        return f'{self.color}'

    def update_remaining(self, wp_qty):
        self.remaining -= wp_qty
        return self.save()


class Order(models.Model):
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, blank=True, null=True)
    roses = models.ForeignKey('Products', on_delete=models.CASCADE, null=True)
    roses_qty = models.IntegerField(verbose_name='Roses Quantity', default=0)
    decoration = models.ForeignKey('Decorations', on_delete=models.CASCADE, null=True)
    decoration_qty = models.IntegerField(verbose_name='Decorations Quantity', default=0)
    wrappingpaper = models.ForeignKey('WrappingPaper', on_delete=models.CASCADE, null=True)
    wp_qty = models.IntegerField(verbose_name='Wrapping Paper Quantity', default=0)
    order_comment = models.ForeignKey('CartItem', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.client} {self.roses} {self.roses_qty} {self.decoration} {self.decoration_qty} {self.wrappingpaper} {self.decoration_qty} {self.order_comment}'

    def total(self):
        roses_price = self.roses.price * self.roses_qty
        decoration_price = self.decoration.price * self.decoration_qty
        wp_price = self.wrappingpaper.price * self.wp_qty
        total_price = roses_price + decoration_price + wp_price
        return round(total_price, 2)


class Client(models.Model):
    first_name = models.CharField(verbose_name='First Name', max_length=30)
    last_name = models.CharField(verbose_name='Last Name', max_length=40)
    client_phone_number = models.ForeignKey('PhoneModel', on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class PhoneModel(models.Model):
    phone_regex = RegexValidator(regex=r'^(\+370|8)\d{8}$')
    phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True, null=True)

    def __str__(self):
        return self.phone_number


class UploadedImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(verbose_name='Order comment', blank=True, null=True)

    def __str__(self):
        return f'Cart {self.id}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.quantity} x {self.product.color}'
