from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='bookstore_home'),
    path('register', views.register, name='register'),
    path('confirmation', views.confirmation, name='registration_confirmation'),
    path('book', views.book_detail, name='book_detail'),
    path('search', views.search, name='search'),
    path('cart', views.cart, name='shopping_cart'),
    path('checkout', views.checkout, name='check_out'),
    path('history', views.history, name='order_history')
]