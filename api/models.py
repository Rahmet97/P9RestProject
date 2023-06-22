from accounts.models import UserData
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['name'])
        ]


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    address = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    picture = models.ImageField(upload_to='pics')

    class Meta:
        indexes = [
            models.Index(fields=['title', 'price', 'address'])
        ]

    def __str__(self):
        return self.title


class ShoppingCard(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Shopping Card'
        verbose_name_plural = 'Shopping Cards'

    def __str__(self):
        return self.product.title


# class UserData(models.Model):
#     phone = models.IntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.user.first_name} {self.user.last_name}'