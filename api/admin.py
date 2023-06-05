from django.contrib import admin
from .models import Product, Category, ShoppingCard, UserData
from modeltranslation.admin import TranslationAdmin


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    pass

admin.site.register((Category, ShoppingCard, UserData))
