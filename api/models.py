from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    address = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.title
