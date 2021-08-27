from shop.models import Contact, Order, OrderUpdate, Product
from django.contrib import admin
# Register your models here.


admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)