from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	customer = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
	image = models.ImageField(null = True, blank = True)
	
	def __str__(self):
		return self.customer.username

