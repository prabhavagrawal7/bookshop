from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='shophome'),
    path('about/', views.about, name='AboutUs'),
    path('contact/', views.contact, name='ContactUs'),
    path('tracker/', views.tracker, name='TrackStatus'),
    path('search/', views.search, name='search'),
    path('products/<int:id>', views.products, name='Products'),
    path('checkout/', views.checkout, name='Checkout'),
    path('handlerequest/', views.handlerequest, name='HandleRequest'),
]