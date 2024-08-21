from django.shortcuts import render, redirect
from .models import Order, Products
from .forms import ImageUploadForm
from .models import UploadedImage
# Create your views here.


def index(request):
    images = UploadedImage.objects.all()
    orders = Order.objects.all()
    product = Order.roses
    product_qty = Order.roses_qty
    decoration = Order.decoration
    decoration_qty = Order.decoration_qty
    wrapping = Order.wrappingpaper
    wp_qty = Order.wp_qty

    context = {
        'images': images,
        'product': product,
        'product_qty': product_qty,
        'decoratio': decoration,
        'decoration_qty': decoration_qty,
        'wrapping': wrapping,
        'wp_qty': wp_qty
    }

    return render(request, template_name='index.html', context=context)


def flower(request):
    flowers = Products.objects.all()
    color = [flower.color for flower in flowers]


    context = {
        'color': color,
    }

    return render(request, template_name='flowers.html', context=context)

