from django.contrib import admin

from .models import (
  Profile,
  Product,
  Status
)

admin.site.register(Status)
admin.site.register(Product)
admin.site.register(Profile)

