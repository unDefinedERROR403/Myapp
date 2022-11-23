from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=200, default='SOME STRING', blank=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def refill(self):
        self.stock += 100
        self.save()


class Client(User):
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'), ]
    company = models.CharField(max_length=50, blank=True)
    shipping_address = models.CharField(max_length=300, null=True,
                                        blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES,
                                default='ON')
    interested_in = models.ManyToManyField(Category)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def interestedin(self):
        return ", ".join([str(i) for i in self.interested_in.all()])

    class Meta:
        verbose_name = "Client"


class Order(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField()
    STATUS_CHOICES = [
        (0, 'Order Cancelled'),
        (1, 'Order Placed'),
        (2, 'Order Shipped'),
        (3, 'Order Delivered')]
    order_status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    status_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.product.name + 'x' + str(self.num_units)

    def total_cost(self):
        return self.product.price * self.num_units


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='profile_images/profile.png', upload_to='profile_images')
    bio = models.TextField(null= True)

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
