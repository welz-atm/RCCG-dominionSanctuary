from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_service/', views.create_service, name='create_service'),
    path('view_service/<int:pk>/', views.view_service, name='view_service'),
    path('view_praise_worship/<int:pk>/', views.view_praise_worship, name='view_praise_worship'),
    path('services/', views.all_services, name='all_services'),
    path('individual_tithe_chart/', views.individual_tithe_chart, name='individual_tithe_chart'),
    path('donations/', views.all_donations, name='all_donations'),
    path('gallery/<int:pk>/', views.view_gallery, name='view_gallery'),
    path('add_image/<int:pk>/', views.add_image_to_service, name='add_image'),
    path('make_donation/', views.create_donation, name='make_donation'),
    path('pay_tithe/', views.pay_tithe, name='pay_tithe'),
    path('confirm_tithe/', views.confirm_tithe, name='confirm_tithe'),
    path('my_tithes/', views.my_tithes, name='my_tithes'),
    path('tithes/', views.all_tithes, name='all_tithes'),
    path('confirm_donation/', views.confirm_donation, name='confirm_donation'),
    path('search/', views.search_view, name='search'),
    path('per_thursday/', views.view_per_thursday, name='per_thursday'),
    path('per_tuesday/', views.view_per_tuesday, name='per_tuesday'),
    path('per_sunday/', views.view_per_sunday, name='per_sunday'),
    path('comment_to_service/', views.add_comment_to_service, name='comment_to_service'),
    path('edit_comment/', views.edit_comment, name='edit_comment'),
]