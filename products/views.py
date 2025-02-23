from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin

from rest_framework.permissions import IsAuthenticated

from .models import Cart, ProductTag, FavoriteProduct, Product, Review, ProductImage
from .serializers import (CartSerializer, ProductTagSerializer,
                          FavoriteProductSerializer, ProductSerializer, ReviewSerializer, ProductImageSerializer)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
    
class ReviewViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs['product_pk'])
    
class FavoriteProductViewSet(ModelViewSet):
    serializer_class = FavoriteProductSerializer
    queryset = FavoriteProduct.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']
    
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
class CartViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class ProductTagViewSet(ModelViewSet):
    serializer_class = ProductTagSerializer
    queryset = ProductTag.objects.all()
    permission_classes = [IsAuthenticated]
    
class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(product__id=self.kwargs['product_pk'])