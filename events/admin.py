from django.contrib import admin
from .models import Event, Category


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
