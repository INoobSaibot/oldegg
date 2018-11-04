from django.contrib import admin

# Register your models here.






from products.models import PaymentCard
from products.models import Brand, Category, Product, ProductInstance, Cart

admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(ProductInstance)
admin.site.register(Cart)
admin.site.register(PaymentCard)
