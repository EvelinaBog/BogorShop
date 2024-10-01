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
    form = OrderForm()

    context = {
        'flowers_data': flowers_data,
        'first_product': first_product,
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def add_to_cart_bulk(request):
    if request.method == 'POST':
        cart = get_or_create_cart(request)  # Get the cart based on session or user
        product_ids = request.POST.getlist('products[]')
        quantities = request.POST.getlist('quantities[]')

        # Process the products and quantities
        for product_id, quantity in zip(product_ids, quantities):
            product = get_object_or_404(Products, id=product_id)
            quantity = int(quantity)

            # Create or update cart items
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('shop:view_cart')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def view_cart(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()  # Get all cart items
    total_price = 0
    for item in cart_items:
        item_total = item.product.price * item.quantity
        total_price += item_total

    return render(request, 'cart.html', {
        'cart': cart,  # Pass the cart object so the comment is available
        'cart_items': cart_items,
        'total_price': round(total_price, 2),  # Send the total price rounded to 2 decimal places
    })


@never_cache
def update_cart_comment(request):
    cart = get_or_create_cart(request)  # Get or create the cart for the session or user

    if request.method == 'POST':
        comment = request.POST.get('comment', '')  # Get the comment from the POST request
        cart.comment = comment  # Update the comment for the cart
        cart.save()  # Save the updated cart
        print(f"Cart comment updated to: {cart.comment}")

    return redirect('shop:view_cart')  # Redirect back to the cart page


@never_cache
def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)

    # Try to delete the specific cart item by its ID
    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass

        # Manually check if the cart has no items left
        if cart.items.count() == 0:  # If there are no items left in the cart
            cart.comment = None  # Reset the comment
            cart.save()  # Save the cart with the reset comment

    return redirect('shop:view_cart')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
