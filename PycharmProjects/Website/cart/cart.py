from django.conf import settings

from shop.models import ProductImage


class Cart:
    """Корзина покупок"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # Сохранить пустую карту в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product_image, quantity=1):
        """Добавить продукт в корзину или обновить его количество"""
        product_id = str(product_image.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product_image.product.price)}

        self.cart[product_id]['quantity'] = quantity

        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product_image):
        """Удаление товара из корзины"""
        product_image_id = str(product_image.id)
        if product_image_id in self.cart:
            del self.cart[product_image_id]
            self.save()

    def __iter__(self):
        """Перебор элементов в корзине и получение продуктов из базы данных"""
        product_ids = self.cart.keys()
        # Получение объектов product и добавление их в корзину
        products_images = ProductImage.objects.filter(id__in=product_ids)
        for product_image in products_images:
            self.cart[str(product_image.id)]['product_image'] = product_image

        for item in self.cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Подсчет всех товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Подсчет стоимости товаров в корзине"""
        return sum(float(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def __contains__(self, item):
        """Проверка принадлежности элемента корзине"""
        is_found = False
        product_ids = self.cart.keys()
        products_images = ProductImage.objects.filter(id__in=product_ids)
        for product_image in products_images:
            if item.id == product_image.product.id:
                is_found = True
                break
        return is_found

    def get_item_price(self, product_image):
        product_id = str(product_image.id)
        if product_id not in self.cart:
            return 0
        return float(self.cart[product_id]['price'])
