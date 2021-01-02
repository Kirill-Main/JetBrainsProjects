from django.urls import path, include

from .views import *

urlpatterns = [
    # path('add/', ProductCreateView.as_view(), name='add'),
    path('by_category/<int:category_id>/', by_category, name='by_category'),
    path('about/<int:product_id>/', about, name='about'),
    path('', index, name='index'),
]
