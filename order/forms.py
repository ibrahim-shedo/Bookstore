from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
	TOWN_CHOICES = (
		('Eastleigh', 'Eastleigh'),
		('South C', 'South C'),
		('Pangani', 'Pangani'),
		('Mombasa CBD', 'Mombasa CBD'),
		('Nakuru Town', 'nakuru Town'),
		('Nairobi CBD', 'Nairobi CBD'),

	)

	CITY_CHOICES = (
		('Nairobi', 'Nairobi'), 
		('Mombasa', 'Mombasa'),
		('Nakuru', 'Nakuru'),
		('Kisumu', 'Kisumu'),
		# ('Kisumu', 'Kisumu'),
		# ('Machakos', 'Machakos'),
		# ('Kakamega', 'Kakagmega'),
		# ('Naivasha', 'Naivasha'),


	)

	PAYMENT_METHOD_CHOICES = (
		('Paypal', 'Paypal'),
		('Credit Card','Credit Card'),
		('Mpesa', 'Mpesa'),

	)

	division = forms.ChoiceField(choices=TOWN_CHOICES)
	district =  forms.ChoiceField(choices=CITY_CHOICES)
	payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect())

	class Meta:
		model = Order
		fields = ['name', 'email', 'phone', 'address', 'division', 'district', 'zip_code', 'payment_method', 'account_no', 'transaction_id']
