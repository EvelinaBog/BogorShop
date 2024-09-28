from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Products, Decorations, CartItem
from .models import UploadedImage
from django.http import JsonResponse
import json


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


def decoration(request):
    dec_data = Decorations.objects.all()
    first_dec = dec_data.first()  # Get the first product

    context = {
        'dec_data': dec_data,
        'first_dec': first_dec  # Pass the first product separately
    }
    return render(request, 'decorations.html', context)


def view_cart(request):
    cart_items = CartItem.object.filter(user=request.user)
    total_price = sum(item.products.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:view_cart')


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart:view_cart')



