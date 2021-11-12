from django import forms
from phonenumber_field.modelfields import PhoneNumberField

class Signup_form(forms.Form):
	username = forms.CharField(max_length=25)
	password = forms.CharField(max_length=25)
	phoneno = forms.CharField(max_length=10)
