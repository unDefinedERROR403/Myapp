# Generated by Django 4.1.2 on 2022-11-24 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='interested_in',
            field=models.ManyToManyField(blank=True, to='myapp.category'),
        ),
    ]