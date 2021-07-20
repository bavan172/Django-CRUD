from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),



    path('', views.home, name="home"),
    path('product/', views.product, name="product"),
    path('customer/<str:pk>/', views.customer, name="customer"),

    path('create/<str:pk>/', views.createOrder, name="create_order"), #place an order from customer page
    path('update/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete/<str:pk>/', views.deleteOrder, name="delete_order"),
]
