from django.shortcuts import render
from decimal import Decimal
from django.conf import settings

from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm



# Create your views here.


def payment_process(request):
	paypal_dict = {
		'business': settings.PAYPAL_RECEIVER_EMAIL,
		

	}
	
	form = PayPalPaymentsForm(initial=paypal_dict)
	return render(request, 'payment/process.html')
		