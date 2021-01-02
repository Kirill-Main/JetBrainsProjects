from django.db import models
from django.contrib.auth.models import User

from shop.models import Product


class Feedback(models.Model):
    """Отзыв на сайте"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')
    content = models.TextField(null=True, blank=True, verbose_name='Описание', max_length=150)
    is_recommended = models.BooleanField(default=True, verbose_name='Главный?')

    def __str__(self):
        return 'Отзыв №{}'.format(self.id)

    def as_json(self):
        return dict(
            username=self.user.username, published=self.published.strftime("%d.%m.%Y"),
            content=self.content, is_recommended=self.is_recommended
        )

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        ordering = ['-published']


# Create your models here.
