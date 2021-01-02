from django.db import models


class Category(models.Model):
    """Выбор категории для продукта"""
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ['name']


class Product(models.Model):
    """Продукт на сайте"""
    title = models.CharField(max_length=50, verbose_name='Продукт')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', null=True, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ['-published']


class ProductImage(models.Model):
    """Продукт с картинкой на сайте"""
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Продукт')
    image = models.ImageField(upload_to='static/images/', verbose_name='Картинка')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    is_main = models.BooleanField(default=False, verbose_name='Главный?')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name_plural = 'Изображения'
        verbose_name = 'Изображение'
        ordering = ['-published']


# Create your models here.
