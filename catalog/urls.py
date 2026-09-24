from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),

    path(
        'categories/',
        views.categories_view,
        name='categories'
    ),

    path(
        'products/',
        views.products,
        name='products'
    ),

    path(
        'category/<slug:slug>/',
        views.category_products,
        name='category_products'
    ),

    path(
        'product/<slug:slug>/',
        views.product_detail,
        name='product_detail'
    ),

    # Panier / السلة
    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'cart/add/<slug:slug>/',
        views.cart_add,
        name='cart_add'
    ),

    path(
        'cart/update/<int:product_id>/',
        views.cart_update,
        name='cart_update'
    ),

    path(
        'cart/remove/<int:product_id>/',
        views.cart_remove,
        name='cart_remove'
    ),

    path(
        'cart/checkout/',
        views.cart_checkout,
        name='cart_checkout'
    ),

    path(
        'contact/',
        views.contact,
        name='contact'
    ),

    path(
        'search/',
        views.search,
        name='search'
    ),
]