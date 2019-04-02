from django.contrib import admin

from .models import Product
from .models import Status

admin.site.register(Status)
admin.site.register(Product)
