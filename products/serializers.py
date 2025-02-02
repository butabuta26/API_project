from rest_framework import serializers
from .models import Product, Cart, ProductsTag, FavoriteProduct
from users.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['created_at', 'updated_at']

class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['user', 'products']

class ProductTagSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = ProductsTag
        fields = ['id', 'name', 'products']

class FavoriteProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = FavoriteProduct
        fields = ['id', 'user', 'products']