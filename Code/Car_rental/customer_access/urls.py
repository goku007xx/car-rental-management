from django.urls import path

from customer_access.views import authentication
from customer_access.views import customer_view

urlpatterns = [
    path('signup/', authentication.signup, name='signup'),
    path('signin/', authentication.signin, name='signin'),
    path('logout/', authentication.logout, name='logout'),

    path('home/', customer_view.home, name = 'home'),
    path('reservation/' , customer_view.reservation, name = 'reservation')
]