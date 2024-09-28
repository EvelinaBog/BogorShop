from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache

from .models import Order, Products, Decorations, CartItem
from .models import UploadedImage


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


def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    qty = int(request.POST.get('quantity', 1))

    if request.user.is_authenticated:
        # Logic for authenticated users
        cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
        cart_item.qty += qty
        cart_item.price = product.price  # Ensure price is updated from product
        cart_item.save()
    else:
        # Logic for anonymous users
        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id]['quantity'] += qty  # Increment quantity
            cart[product_id]['price'] = str(product.price)  # Update price to reflect changes
        else:
            cart[product_id] = {
                'quantity': qty,
                'price': str(product.price)  # Store the price as a string
            }

        request.session['cart'] = cart  # Save updated cart back to session
        request.session.modified = True  # Mark session as modified

    return redirect('shop:view_cart')


@never_cache
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        product = get_object_or_404(Products, id=product_id)  # Retrieve product info
        qty = item['quantity']
        item_price = product.price * qty  # Calculate the total price for this item
        total_price += item_price
        cart_items.append({
            'id': product_id,
            'color': product.color,
            'qty': qty,
            'price': item_price
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
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
