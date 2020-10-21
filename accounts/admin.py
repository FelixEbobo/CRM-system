from django.contrib import admin

# Register your models here.
from .models import Tag, customer, product, order

admin.site.register(customer)
admin.site.register(product)
admin.site.register(order)
admin.site.register(Tag)