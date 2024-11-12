from django.urls import path
from .import views

urlpatterns = [
    path('login',views.log),
    path('register',views.reg)
]
