from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_page, name="login_page"),
    path('register/', views.register_page, name="register_page"),
    path('logout/', views.logout_page, name="logout_page"),

    path('', views.home, name="home_page"),
    path('user/', views.user_page, name="user_page"),
    path('profile/', views.account_settings, name="user_profile"),
    path('product/', views.product, name="product_page"),
    path('customer/<str:pk>', views.customer, name="customer_page"),

    path('create_order/<str:pk>/', views.create_order, name="create_order_form"),
    path('update_order/<str:pk>/', views.update_order, name="update_order_form"),
    path('delete_order/<str:pk>/', views.delete_order, name="delete_order_form"),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_complete")

]
