# Generated by Django 4.2.1 on 2023-05-27 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_product_address_af_remove_product_address_ar_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='api_categor_name_53a3ad_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['title', 'price', 'address'], name='api_product_title_cf79af_idx'),
        ),
    ]
