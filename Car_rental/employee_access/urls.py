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
    path('approve_reservation/', employee_view.approve_reservation, name='approve_reservation'),
    path('view_approve/',employee_view.view_approve, name ='view_approve'),
    path('update_rent_later/',employee_view.update_rent_later , name = 'update_rent_later'),
    path('payment/' , employee_view.payment, name = 'payment')
]