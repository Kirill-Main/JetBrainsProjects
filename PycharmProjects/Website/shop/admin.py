from django.contrib import admin

from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'category')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

# Register your models here.
