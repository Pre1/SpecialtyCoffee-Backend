from django.contrib import admin

from .models import (
  Profile,
  Product,
  Status,
  OrderProduct,
  Order,
)

admin.site.register(Status)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(OrderProduct)
admin.site.register(Order)

