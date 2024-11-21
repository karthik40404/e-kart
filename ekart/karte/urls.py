from django.urls import path
from .import views

urlpatterns = [
    path('',views.log),
    path('shop_home',views.shop_home),
    path('register',views.reg),
    path('logout',views.log_out),
    path('add',views.addproduct),
    path('edit_product/<pid>',views.edit_product),
    path('delete_product/<pid>',views.delete_product),
    path('uhome',views.uhome),
    path('viewproduct/<pid>',views.viewp),
    path('addc/<pid>',views.addtocart),
    path('viewc',views.viewc),
]
