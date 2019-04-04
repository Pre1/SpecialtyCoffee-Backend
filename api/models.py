from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
	customer = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.customer.username



"""
Status options:

- New
- In Progress 
- Completed
- Canceled
- On Hold

"""
class Status(models.Model):
	title = models.CharField(max_length=120)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.title


class Product(models.Model):
	"""
	Description: Product
	"""
	name = models.CharField(max_length=120)
	process = models.CharField(max_length=120)
	flavor = models.CharField(max_length=120)
	origin = models.CharField(max_length=120)
	description = models.TextField()
	# 123.12
	price = models.DecimalField(max_digits=5, decimal_places=2)
	image = models.ImageField(null=True, blank=True)
	is_avaliable = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	added_by = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['-created_at', ]



"""
order = [
	{status},
	{ordered_by},
	[{order_products}],
]	
"""

class Order(models.Model):
	"""
	Description: Order
	"""
	status = models.ForeignKey(
		Status,
		default=1, 
		on_delete=models.CASCADE,
		related_name='orders_status')

	ordered_by = models.ForeignKey(
		Profile,
		default=1, 
		on_delete=models.CASCADE,
		related_name='customer_orders')

	total_price = models.DecimalField(max_digits=5,default=0.0, decimal_places=2)

	created_at = models.DateTimeField(auto_now_add=True)

	def set_total_price(self):
		print("========Order Model========")
		print("self.order_products.all(): ", self.order_products.values_list('total_price', flat=True))
		print("sum: ", sum(self.order_products.all().values_list('total_price', flat=True)))
		print("total price: ", self.total_price)
		print("========Order Model========")

		self.total_price = sum(self.order_products.all().values_list('total_price', flat=True))
		self.save()
		print("total price: ", self.total_price)


	def __str__(self):
		return "id: {} => order by: {}".format(self.id, self.ordered_by.customer.username)

	class Meta:
		ordering = ['-created_at', ]




"""
cart = [
	{OrderProduct1},
	{OrderProduct2},
	{OrderProduct3},
]	
"""

class OrderProduct(models.Model):
	"""
	Description: OrderProduct
	"""

	order = models.ForeignKey(
		Order, 
		default=1, 
		on_delete=models.CASCADE, 
		related_name='order_products')

	product = models.ForeignKey(
		Product, 
		default=1, 
		on_delete=models.CASCADE)

	quantity = models.PositiveIntegerField(default=1)

	total_price = models.DecimalField(max_digits=5, default=0.0, decimal_places=2)

	def get_price(self):
		return self.product.price * self.quantity

	def __str__(self):
		return "Product: {} || quantity: {}".format(self.product.name, self.quantity)



@receiver(post_save, sender=OrderProduct)
def get_price(instance, *args, **kwargs):
	print("===================")
	print(vars(instance))
	print("===================")

	print("instance.product.price: ", instance.product.price)
	print("instance.quantity: ", instance.quantity)
	total_price = instance.product.price * instance.quantity
	instance.total_price = total_price
	print("total_price: ", total_price)

	instance.order.set_total_price()


