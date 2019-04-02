from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	customer = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
	image = models.ImageField(null = True, blank = True)
	
	def __str__(self):
		return self.customer.username


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
		ordering = ['-created_at',]


