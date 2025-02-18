from django.urls import path
from products.views import ProductViewSet, ReviewViewSet, CartViewSet, ProductTagViewSet, FavoriteProductViewSet, ProductImageViewSet

urlpatterns = [
    path('products/', ProductViewSet.as_view(), name="products"),
    path('products/<int:pk>/', ProductViewSet.as_view(), name='product'),
    path('products/<int:product_id>/images/', ProductImageViewSet.as_view(), name='images'),
    path('products/<int:product_id>/images/<int:pk>', ProductImageViewSet.as_view(), name='image'),
    path('products/<int:pk>/reviews/', ReviewViewSet.as_view(), name="reviews"),
    path('cart/', CartViewSet.as_view(), name='cart'),
    path('products/<int:pk>/tags/', ProductTagViewSet.as_view(), name='tags'),
    path('tags/', ProductTagViewSet.as_view(), name='tags'),
    path('favorites/', FavoriteProductViewSet.as_view(), name='favorites')
]
