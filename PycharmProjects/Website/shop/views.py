import json

from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse

from accounts.models import Feedback
from cart.forms import CartAddProductForm
from .models import *
from .forms import ProductForm


class ProductCreateView(CreateView):
    template_name = 'products/create.html'
    form_class = ProductForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


def index(request):
    products_images = ProductImage.objects.filter(is_main=True)
    context = {'products_images': products_images}
    return render(request, 'products/index.html', context)


def by_category(request, category_id):
    products_images = ProductImage.objects.filter(is_main=True, product__category_id=category_id)
    has_products_in_directory = products_images.exists()
    current_category = Category.objects.get(pk=category_id)
    context = {
        'products_images': products_images, 'current_category': current_category,
        'category_id': category_id, 'has_products_in_directory': has_products_in_directory,
    }
    return render(request, 'products/by_category.html', context)


def about(request, product_id):
    current_product = Product.objects.get(pk=product_id)
    current_product_images = ProductImage.objects.filter(product_id=product_id)
    cart_product_form = CartAddProductForm()
    context = {
        'current_product_images': current_product_images, 'current_product': current_product,
        'cart_product_form': cart_product_form,
    }

    if request.method == 'POST' and request.is_ajax() and request.user.is_authenticated:
        message = request.POST['message']
        is_recommended = request.POST['is_recommended'] == 'yes'
        user = request.user
        data = {}

        feedback, created = Feedback.objects.update_or_create(
            user=user, product=current_product,
            content=message, is_recommended=is_recommended
        )

        if created:
            data['feedback'] = feedback.as_json()
            data['feedbacks_count'] = len(Feedback.objects.filter(product__id=product_id))
            return HttpResponse(json.dumps(data), content_type='application/json')

    context['feedbacks'] = Feedback.objects.filter(product__id=product_id)
    context['feedbacks_count'] = len(context['feedbacks'])

    return render(request, 'products/about.html', context)

# Create your views here.
