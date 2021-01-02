from django.db import models
from django.contrib.auth.models import User

from shop.models import ProductImage


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    city = models.CharField(max_length=100, verbose_name='Город', default='')
    address = models.CharField(max_length=250, verbose_name='Адрес', default='')
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс', default='')
    has_paid = models.BooleanField(default=False, verbose_name='Оплатил?')

    class Meta:
        ordering = ['-created']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ №{}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.PROTECT, verbose_name='Заказ')
    product = models.ForeignKey(ProductImage, related_name='order_items',
                                on_delete=models.PROTECT, verbose_name='Продукт')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name_plural = 'Элементы заказов'
        verbose_name = 'Элемент заказа'


# Create your models here.
