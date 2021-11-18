from django.urls import path
from django.conf.urls import include, url

from customer_access.views import authentication
from customer_access.views import customer_view

urlpatterns = [
    path('signup/', authentication.signup, name='signup'),
    path('signin/', authentication.signin, name='signin'),
    path('logout/', authentication.logout, name='logout'),
    path('testing/' , authentication.testing , name = 'testing'),
    path('home/', customer_view.home, name = 'home'),
    path('reservation/' , customer_view.reservation, name = 'reservation'),
    path('vehicle_submission/' , customer_view.vehicle_submission, name = 'vehicle_submission'),
    path('view_reservations/' , customer_view.view_reservations , name = 'view_reservations')
    #path('vehicle/' , customer_view.vehicle, name = 'vehicle')
]