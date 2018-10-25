from django.contrib import admin

# Register your models here.







from cart.models import CartItem, TestCart

admin.site.register(CartItem)
admin.site.register(TestCart)

