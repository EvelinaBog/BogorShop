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


# Create your models here.


def resize_image(image, size=(1080, 1080)):
    img = PilImage.open(image)
    original_size = img.size

    # Convert to RGB if the image has an alpha channel
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    img.thumbnail(size, PilImage.Resampling.LANCZOS)
    resized_size = img.size

    print(f"Original size: {original_size}, Resized size: {resized_size}")

    img_io = io()
    img.save(img_io, format='PNG', quality=50)  # Adjust quality as needed
    img_io.seek(0)  # Rewind the file pointer

    img_file = InMemoryUploadedFile(
        img_io,
        'ImageField',
        image.name,
        'image/jpeg',
        img_io.getbuffer().nbytes,
        None
    )
    print(f"File size after resize: {img_file.size} bytes")
    return img_file


class Products(models.Model):
    color = models.CharField(verbose_name='Color', max_length=20)
    remaining = models.FloatField(verbose_name='Remaining', default=0)
    price = models.FloatField(verbose_name='Price', default=1.30)
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

    def __str__(self):
        return f'{self.type}'

    def update_remaining(self, decoration_qty):
        self.remaining -= decoration_qty
        return self.save()


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

    def __str__(self):
        return f'{self.client} {self.roses} {self.roses_qty} {self.decoration} {self.decoration_qty} {self.wrappingpaper} {self.decoration_qty}'

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
