from django.urls import path
from django.conf.urls import include, url

from employee_access.views import authentication
from employee_access.views import employee_view

urlpatterns = [
    path('signin/', authentication.signin, name='signin'),
    path('home/', employee_view.home, name = 'home'),
    path('logout/', authentication.logout, name='logout'),
    path('view_res/' , employee_view.view_res , name = 'view_res'),
    path('cancel_reservation/', employee_view.cancel_reservation, name='cancel_reservation'),
    #path('vehicle/' , customer_view.vehicle, name = 'vehicle')
]