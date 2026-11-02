from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('order/', views.order_page, name='order'),
    path('success/<int:order_id>/', views.success, name='success'),
    path('orders/', views.order_list, name='order_list'),
    path('mark-delivered/<int:order_id>/', views.mark_delivered, name='mark_delivered'),
    path('out-for-delivery/<int:order_id>/', views.mark_out_for_delivery, name='mark_out_for_delivery'),
    path('mark-paid/<int:order_id>/', views.mark_paid, name='mark_paid'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('edit/<int:order_id>/', views.edit_order, name='edit_order'),
    path('report/', views.daily_report, name='daily_report'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('track/', views.track_order, name='track_order'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
]