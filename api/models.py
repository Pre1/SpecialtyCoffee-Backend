from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

class Profile(models.Model):
	# from fk to 1to1
	customer = models.OneToOneField(User, on_delete=models.CASCADE)
	# customer = models.OneToOneField(User, default=1, on_delete=models.CASCADE)
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
	# added_by = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

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
		on_delete=models.CASCADE,
		related_name='customer_orders')

	total_price = models.DecimalField(max_digits=15,default=0.0, decimal_places=2)

	created_at = models.DateTimeField(auto_now_add=True)

	def set_total_price(self):
		print("========Order Model========")
		print("self.order_products.all(): ", 
			self.order_products.all())
		print("sum: ", sum(self.order_products.all().values_list('total_price', flat=True)))
		print("BEFORE total price: ", self.total_price)
		

		self.total_price = sum(self.order_products.all().values_list('total_price', flat=True))
		self.save()
		print("AFTER total price: ", self.total_price)
		print("========Order Model========")

	def __str__(self):
		return "id: {} || order by: {} || total_price: {}".format(
			self.id,
			self.ordered_by.customer.username,
			self.total_price,
		)

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

	total_price = models.DecimalField(max_digits=15, default=0.0, decimal_places=2)

	def __str__(self):
		return "OrderProduct ID: {} || Product ID: {} || quantity: {} || total_price: {}".format(
			self.id,
			self.product.id, 
			self.quantity,
			self.total_price,
		)


## Signals ##

# after chaning it to pre_save
@receiver(post_save, sender=OrderProduct)
@receiver(post_delete, sender=OrderProduct)
def get_price(instance, *args, **kwargs):
	# post save and post delete signal
	instance.order.set_total_price()


# @receiver(post_save, sender=User)
# def create_profile(instance, *args, created, **kwargs):
# 	print("========Profile Creations========")
# 	if created:
# 		print("pre")
# 		Profile.objects.create(customer=instance)


