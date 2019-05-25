from django.conf.urls import url,include
from myapp import views

# SET THE NAMESPACE!
app_name = 'myapp'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^about/$', views.about,name='about'),
    url(r'^paypal_home/$', views.paypal_home,name='paypal_home'),
    url(r'^download/$', views.download,name='download'),
    url(r'^profile/$', views.view_profile,name='view_profile'),
    url(r'^paypal/',include('paypal.standard.ipn.urls')),
    url(r'^edit$', views.edit_profile,name='edit_profile'),
    url(r'^change_password$', views.change_password,name='change_password'),
    url(r'^pdf$', views.pdf,name='pdf'),
    
]
