from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm


@login_required(login_url='/login/')
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        user = request.user
        city = request.POST['city']
        address = request.POST['address']
        postal_code = request.POST['postal_code']
        order = Order(user=user, city=city,
                      address=address, postal_code=postal_code)
        order.save()
        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product_image'],
                                     price=item['price'],
                                     quantity=item['quantity'])
            # очистка корзины
        cart.clear()
        return render(request, 'orders/created.html',
                      {'order': order})

    return render(request, 'orders/create.html')

# Create your views here.
