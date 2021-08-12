from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_service/', views.create_service, name='create_service'),
    path('view_service/<int:pk>/', views.view_service, name='view_service'),
    path('services/', views.all_services, name='all_services'),
    path('gallery/<int:pk>/', views.view_gallery, name='view_gallery'),
    path('add_image/<int:pk>/', views.add_image_to_service, name='add_image'),
    path('make_donation/', views.create_donation, name='make_donation'),
    path('pay_tithe/', views.pay_tithe, name='pay_tithe'),
    path('pay_tithes/', views.test_pay_tithes, name='pay_tithes'),
    path('confirm_tithe/', views.confirm_tithe, name='confirm_tithe'),
    path('my_tithes/', views.my_tithes, name='my_tithes'),
    path('tithes/', views.all_tithes, name='all_tithes'),
    path('confirm_donation/', views.confirm_donation, name='confirm_donation'),
    path('search/', views.search_view, name='search'),
]