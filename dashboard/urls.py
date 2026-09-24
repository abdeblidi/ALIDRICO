from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('', views.home, name='home'),

    path(
        'subcategories/',
        views.subcategories,
        name='subcategories'
    ),

    path(
        'orders/statistics/',
        views.order_statistics,
        name='order_statistics'
    ),

]
