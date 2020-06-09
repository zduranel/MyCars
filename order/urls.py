from django.urls import path

from django.test import TestCase

# Create your tests here.
from . import views

urlpatterns = [
    path('orderproduct',views.orderproduct, name='orderproduct'),
    path('addtocart/<int:id>', views.addtocart, name='addtocart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name ='deletefromcart')

]