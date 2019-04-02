from django.db import models
from django.contrib.auth.models import User


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
		ordering = ['-created_at',]


# class Order(models.Model):
#     """
#     Description: Order
#     """
    
#     status = models.ForeignKey(Status, default=1, on_delete=models.CASCADE)

#     class Meta:
#         pass