from django.forms import ModelForm

from .models import *


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'content', 'price', 'category')