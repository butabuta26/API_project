from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView

from rest_framework.permissions import IsAuthenticated

from .models import Cart, ProductTag, FavoriteProduct, Product, Review
from .serializers import CartSerializer, ProductTagSerializer, FavoriteProductSerializer, ProductSerializer, ReviewSerializer

class ProductViewSet(RetrieveModelMixin, 
                    CreateModelMixin,
                    ListModelMixin,
                    UpdateModelMixin,
                    DestroyModelMixin,
                    GenericAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    
    
class ReviewViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get(self, request, pk=None, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CartViewSet(CreateModelMixin, ListModelMixin, GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        cart = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(user=self.request.user, cart=cart)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductTagViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
    serializer_class = ProductTagSerializer

    def get_queryset(self):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return product.tags.all()

    def perform_create(self, serializer):
        tag = serializer.save()
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        product.tags.add(tag)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class FavoriteProductViewSet(CreateModelMixin, ListModelMixin, GenericAPIView):
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteProduct.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)