from django.urls import path
from .import views

urlpatterns = [
    path('',views.log),
    path('shop_home',views.shop_home),
    path('register',views.reg)
]