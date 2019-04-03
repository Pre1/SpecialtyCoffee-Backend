from django.db import models
from django.contrib.auth.models import User


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
		User,
		default=1, 
		on_delete=models.CASCADE,
		related_name='customer_orders')

	total_price = models.DecimalField(max_digits=5,default=0.0, decimal_places=2)

	created_at = models.DateTimeField(auto_now_add=True)

	def get_total_price(self):
		print(self.order_products)
		# return sum(self.order_products)

	def __str__(self):
		return "id: {} => order by: {}".format(self.id, self.ordered_by.username)

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

