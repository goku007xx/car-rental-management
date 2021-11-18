from django.urls import path
from django.conf.urls import include, url

from customer_access.views import authentication
from customer_access.views import customer_view

urlpatterns = [
    path('signin/', authentication.signin, name='signin')
    #path('logout/', authentication.logout, name='logout'),
    #path('vehicle/' , customer_view.vehicle, name = 'vehicle')
]