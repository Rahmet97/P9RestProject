from django.contrib import admin
from .models import Product, Category, ShoppingCard

admin.site.register((Product, Category, ShoppingCard))
