from django.urls import path
from products.views import ProductViewSet, ReviewViewSet, CartViewSet, ProductTagViewSet, FavoriteProductViewSet

urlpatterns = [
    path('products/', ProductViewSet.as_view(), name="products"),
    path('products/<int:pk>/', ProductViewSet.as_view(), name='product'),
    path('reviews/', ReviewViewSet.as_view(), name="reviews"),
    path('cart/', CartViewSet.as_view(), name='cart'),
    path('products/<int:pk>/tags/', ProductTagViewSet.as_view(), name='tags'),
    path('favorites/', FavoriteProductViewSet.as_view(), name='favorites')
]
