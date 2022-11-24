from django.contrib import admin

import myapp.models
from myapp.models import Product, Category, Client, Order, Profile

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Profile)


class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'category', 'price', 'stock', 'available']
    list_display = ('name', 'category', 'price', 'stock', 'available')
    actions = ['add_product']

    @admin.action(description='Add 50 to the stock field')
    def add_product(self, request, queryset):
        for product in queryset:
            product.stock += 50
            if not product.available:
                product.available = True

            product.save()


admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)


class ClientAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'city']
    list_display = ('first_name', 'last_name', 'city', 'interestedin')


admin.site.unregister(Client)
admin.site.register(Client, ClientAdmin)
