import json

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from shop.models import ProductImage
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product_image = ProductImage.objects.get(product_id=product_id, is_main=True)

    if request.is_ajax():
        quantity = int(request.POST['quantity'])
        cart.add(product_image=product_image, quantity=quantity)
        data = {'cart_total_price': cart.get_total_price(), 'item_price': cart.get_item_price(product_image),
                'cart_length': len(cart)}
        data['item_total_price'] = quantity * data['item_price']
        return HttpResponse(json.dumps(data), content_type='application/json')

    quantity = 1
    cart.add(product_image=product_image, quantity=quantity)

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = ProductImage.objects.get(product_id=product_id, is_main=True)
    cart.remove(product)
    if len(cart) > 0:
        return redirect('cart:cart_detail')
    return redirect("/")


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

# Create your views here.
