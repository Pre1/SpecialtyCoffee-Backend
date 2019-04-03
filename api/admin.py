from django.contrib import admin

from .models import (
  Profile,
  Product,
  Status,
  OrderProduct,
  Order,
)

class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'price', 'is_avaliable']

class OrderProductAdmin(admin.ModelAdmin):
	list_display = ['product', 'quantity', 'order', 'total_price']

class OrderProductInline(admin.StackedInline):
	model = OrderProduct
	extra = 0

class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'ordered_by', 'total_price', 'status']
	inlines = [OrderProductInline]

admin.site.register(Status)
admin.site.register(Product, ProductAdmin)
admin.site.register(Profile)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Order, OrderAdmin)



