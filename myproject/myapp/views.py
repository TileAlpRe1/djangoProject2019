from django.shortcuts import render, redirect
from myapp.forms import UserForm,UserProfileInfoForm,EditProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
#from myapp.forms import EditProfileForm

from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm

from django.http import FileResponse
from django.utils.text import slugify
from django.utils import timezone

import os
from django.conf import settings
from django.http import HttpResponse, Http404

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm


# Create your views here.

def index(request):
    return render(request,'myapp/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

	
# def payment_done(request):
    # return render(request, 'payment/done.html')

# def payment_canceled(request):
    # return render(request, 'payment/canceled.html')	
	
def about(request):
    return render(request,'myapp/about.html')

def payment_site(request):
    return render(request,'myapp/payment_site.html')

# def download(request):
    # return render(request,'myapp/download.html')

def paypal_home(request):
    args = {}
    host = request.get_host()
    
    paypal_dict = {
	    'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '59.00',
        'currency': 'EUR',
        'item_name': 'Insurance Fee',
        'invoice': 'unique-Invoice-00001',
        # 'norify_url': '127.0.0.1:8000/myapp/a-very-hard-to-guess-url',
        # 'return_url': '127.0.0.1:8000/myapp/paypal_return',
        # 'cancel_return': '127.0.0.1/8000/myapp/paypal_cancel',
    }
	
    ee = PayPalPaymentsForm(initial=paypal_dict)
    args={'ee': ee}
    return render (request,'myapp/paypal_home.html',args)


@csrf_exempt
def paypal_return(request):
    #args = {'post': request.POST, 'get': request.GET}
    return render(request,'myapp/paypal_return.html')

@csrf_exempt	
def paypal_cancel(request):
    #args = {'post': request.POST, 'get': request.GET}
    return render(request,'myapp/paypal_cancel.html')
	
	
def download(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename= "TEST.pdf"

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
	#content = "Hello World"
    p.drawString(100, 800, "You are officially fully insured")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response 
	
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'Official_Paper' in request.FILES:
                print('found it')
                profile.Official_Paper = request.FILES['Official_Paper']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'myapp/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

						   
						   
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'myapp/view_profile.html', args)

	
def edit_profile(request):
    if request.method == 'POST':
        user = EditProfileForm(request.POST, instance=request.user)

        if user.is_valid():
            user.save()
            return redirect(reverse('myapp:view_profile'))
    else:
        user = EditProfileForm(instance=request.user)
        args = {'user': user}
    return render(request, 'myapp/edit_profile.html', args)


	
	
	

def insurance_confirmation(request):
        return render(request,'myapp/insurance_confirmation.html')	
	
def change_password(request):
    if request.method == 'POST':
        user = PasswordChangeForm(data=request.POST, user=request.user)

        if user.is_valid():
            user.save()
            update_session_auth_hash(request, user.user)
            return redirect(reverse('myapp:view_profile'))
        else:
            return redirect(reverse('myapp:change_password'))
    else:
        user = PasswordChangeForm(user=request.user)
        args = {'user': user}
        return render(request, 'myapp/change_password.html', args)

def pdf(request):
    today = timezone.now()
    params = {'today': today}
    return render(request,'myapp/pdf.html',params)
	
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'myapp/login.html', {})
