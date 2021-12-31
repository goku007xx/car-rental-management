from django.contrib import admin
from django.db.models import fields
# Register your models here.

from .models import Vehicle, Employee , Outlet_Contact

class VehicleAdmin(admin.ModelAdmin):
    fields = ['plate_number' , 'model', 'no_of_seats' ,'ac' ,  'vehicle_status' , 'cost_per_day' , 'outlet']

class EmployeeAdmin(admin.ModelAdmin):
    fields = [ 'employee_name' ,'employee_password' ,'employee_phone_no' ,'outlet' ]

class OutletcontactAdmin(admin.ModelAdmin):
    fields = [ 'outlet_phone' ,'outlet_mail' ]


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Outlet_Contact, OutletcontactAdmin)
