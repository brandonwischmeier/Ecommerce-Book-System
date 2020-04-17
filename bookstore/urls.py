from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

appname = 'bookstore'

urlpatterns = [
    path('', views.home, name='bookstore_home'),
    path('register', views.register, name='register'),
    path('confirmation', views.confirmation, name='registration_confirmation'),
    path('login_failure', views.login_failure, name='login_failure'),
    path('activate/<slug:uidb64>/<slug:token>/',
         views.activate, name='activate'),
    path('book',views.book_detail,name='book_detail'),
    path('book/(?P<pk>\d+)',views.book_detail,name='book_detail_with_pk'),
    path('search', views.search, name='search'),
    path('cart', views.cart, name='shopping_cart'),
    path('add/(?P<pk>\d+)', views.add_to_cart, name = 'add_to_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('history', views.history, name='order_history'),
    path('login', views.loginU, name='login'),
    path('logout', views.logoutU, name='logout'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('profile/edit/password', views.edit_password, name='edit_password'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="bookstore/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="bookstore/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="bookstore/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="bookstore/password_reset_done.html"),
         name="password_reset_complete"),
]
