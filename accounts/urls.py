from django.urls import path
from django.http import HttpResponse
from . import views


urlpatterns = [
    path('', views.home, name="Home"),
    path('customer/<str:pk>', views.customer1, name='Customer'),
    path("products/", views.products, name="Products"),
    path("create_order/", views.create_order, name="CreateOrder"),
    path("update_order/<str:pk>/", views.update_order, name="UpdateOrder"),
    path("delete_order/<str:pk>/", views.delete_order, name="DeleteOrder"),
    path("register/", views.register_page, name="RegisterPage"),
    path("login/", views.login_page, name="LoginPage"),
    path("logout/", views.logout_user, name='LogoutUser'),
    path('user/', views.user_page, name="UserPage"),
]
