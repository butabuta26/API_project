from django.urls import path
from products.views import products_view, cart_view, product_tag_view, favorite_product_view

urlpatterns = [
    path('products/', products_view, name='products'),
    path('cart/', cart_view, name='cart'),
    path('tags/', product_tag_view, name='tags'),
    path('favorites/', favorite_product_view, name='favorites')
]
