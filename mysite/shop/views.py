from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache

from .models import Order, Products, Decorations, CartItem, Cart
from .models import UploadedImage
from django.utils.decorators import decorator_from_middleware
from django.middleware.cache import CacheMiddleware
from django.views.decorators.cache import cache_control
from .forms import OrderForm


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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def flower(request):
    flowers_data = Products.objects.all()
    first_product = flowers_data.first()
    order_comment = Order.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the Order model
            return redirect('flower')  # Redirect to prevent form re-submission
    else:
        form = OrderForm()

    context = {
        'flowers_data': flowers_data,
        'first_product': first_product,  # Pass the first product separately
        'order_comment': order_comment,
        'form': form,
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


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key or request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def add_to_cart_bulk(request):
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        product_ids = request.POST.getlist('products[]')
        quantities = request.POST.getlist('quantities[]')

        for product_id, quantity in zip(product_ids, quantities):
            product = get_object_or_404(Products, id=product_id)
            quantity = int(quantity)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()

    return redirect('shop:view_cart')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def view_cart(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': round(total_price, 2)
    })


@never_cache
def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass
    else:
        cart = request.session.get('cart', {})
        if str(item_id) in cart:
            del cart[str(item_id)]

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('shop:view_cart')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
