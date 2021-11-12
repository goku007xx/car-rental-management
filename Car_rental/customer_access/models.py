from django.db import models

class Customer(models.Model):
	customer_id = models.AutoField(primary_key = True)
	username = models.CharField(max_length = 25)
	password = models.CharField(max_length = 25)
	phone_no = models.CharField(unique=True,max_length=10)

	class Meta:
		db_table = 'customer'

class Outlet(models.Model):
	outlet_id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 25)
	location = models.CharField(max_length = 25)
	outlet_savings = models.IntegerField()

	class Meta:
		db_table = 'outlet'

class Employee(models.Model):
	employee_id = models.AutoField(primary_key = True)
	employee_name = models.CharField(max_length = 25)

	outlet = models.ForeignKey(Outlet,on_delete=models.PROTECT)

	class Meta:
		db_table = 'employee'

class Vehicle(models.Model):
	plate_number = models.CharField(max_length = 25,primary_key = True)
	model = models.CharField(max_length = 25)
	no_of_seats = models.IntegerField()
	ac = models.BooleanField()
	vehicle_status = models.CharField(max_length = 25)

	outlet = models.ForeignKey(Outlet,on_delete=models.PROTECT)

	class Meta:
		db_table = 'vehicle'

class Reservation(models.Model):
	reservation_id = models.AutoField(primary_key = True)
	reservation_date = models.DateField()
	vehicle_taken_date = models.DateField()
	expected_return_date = models.DateField()
	advance = models.IntegerField(default = 1000)
	reservation_status = models.CharField(max_length = 25)

	customer = models.ForeignKey(Customer,default = -1 ,on_delete=models.SET_DEFAULT)
	outlet = models.ForeignKey(Outlet,on_delete=models.PROTECT)
	plt_no = models.ForeignKey(Vehicle,default='car sold/no more',on_delete = models.SET_DEFAULT)
	emp = models.ForeignKey(Employee , default = -1 , on_delete = models.SET_DEFAULT)

	class Meta:
		db_table = 'reservation'

class Rent(models.Model):
	bill_id = models.AutoField(primary_key = True)
	taken_date = models.DateField()
	return_date = models.DateField()
	no_of_days = models.IntegerField()
	tax_amt = models.IntegerField(default =10)
	total_amt = models.IntegerField()
	refund = models.IntegerField()

	customer = models.ForeignKey(Customer,default = -1 ,on_delete=models.SET_DEFAULT) # Check This
	reservation = models.ForeignKey(Reservation,unique=True,default = -1,on_delete=models.PROTECT)
	plt_no = models.ForeignKey(Vehicle,default='car sold/no more',on_delete = models.SET_DEFAULT)

	class Meta:
		db_table = 'rent'

class Discount(models.Model):
	promo_id = models.CharField(max_length = 30,primary_key = True)
	discount_amount = models.IntegerField()
	start_date = models.DateField()
	end_date = models.DateField()

	class Meta:
		db_table = 'discount'

class Outlet_Contact(models.Model):
	outlet_phone = models.CharField(max_length = 10,primary_key = True)
	outlet_mail = models.EmailField()
	
	outlet = models.ForeignKey(Outlet,on_delete=models.CASCADE)

	class Meta:
		db_table = 'outlet_contact'

# Create your models here.
