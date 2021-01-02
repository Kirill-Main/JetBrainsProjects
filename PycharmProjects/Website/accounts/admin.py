from django.contrib import admin

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'published', 'content')
    list_display_links = ('user', 'published')
    search_fields = ('user', 'published')


admin.site.register(Feedback, FeedbackAdmin)

# Register your models here.
