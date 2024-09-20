from django.shortcuts import render, redirect, get_object_or_404
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
    flowers_data = Products.objects.all()
    first_product = flowers_data.first()  # Get the first product

    context = {
        'flowers_data': flowers_data,
        'first_product': first_product  # Pass the first product separately
    }
    return render(request, 'flowers.html', context)


def order_products(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    form = AddToCartForm()  # Create the form instance

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            # Add your logic to handle adding the product to the cart here

    return render(request, 'flowers.html', {'form': form, 'product': product})

