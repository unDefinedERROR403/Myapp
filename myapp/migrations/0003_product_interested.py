# Generated by Django 4.1.2 on 2022-11-09 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_category_warehouse_product_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='interested',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
