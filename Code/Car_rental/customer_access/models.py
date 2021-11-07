from django.db import models


class Customer(models.Model):
	username = models.CharField(max_length = 25)
	password = models.CharField(max_length = 25)
	phone_no = models.CharField(unique=True,max_length=10)
	class Meta:
		db_table = 'customer'

class Outlet(models.Model):
	outlet_id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 25)
	location = models.CharField(max_length = 25)

	class Meta:
		db_table = 'outlet'

# Create your models here.
