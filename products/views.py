from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from products.models import Product, Cart, ProductsTag, FavoriteProduct
from products.serializers import ProductSerializer, CartSerializer, ProductTagSerializer, FavoriteProductSerializer

@api_view(['GET', 'POST'])
def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({'id': product.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
@api_view(['GET', 'POST'])
def cart_view(request):
    if request.method == 'GET':
        cart_items = Cart.objects.all()
        cart_items_list = []
        
        for cart_item in cart_items:
            cart_item_data = {
                'products': ProductSerializer(cart_item.products.all(), many=True).data

            }
            cart_items_list.append(cart_item_data)
            
        return Response({'cart_items': cart_items_list})
    elif request.method == 'POST':
        data = request.data
        serializer = CartSerializer(data=data)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        if int(quantity) <= 0:
            return Response({'error': 'Quantity must be a positive integer'}, status=status.HTTP_400_BAD_REQUEST)
        
        product = get_object_or_404(Product, id=product_id)
        Cart.products.add(product)
        serializer = CartSerializer(Cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def product_tag_view(request):
    product_id = request.data.get('product_id')

    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'GET':
        tags = product.produc_tags.all()
        return Response({'product_id': product_id, 'tags': list(tags.values())})
    
    elif request.method == 'POST':
        tag_name = request.data.get('tag_name')
        if not tag_name:
            return Response({'error': 'Tag name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        tag, created = ProductsTag.objects.get_or_create(name=tag_name)
        product.produc_tags.add(tag)
        serializer = ProductTagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def favorite_product_view(request):
    if request.method == 'GET':
        favorites = FavoriteProduct.objects.filter(user=request.user)
        return Response({'user': request.user.id, 'favorites': list(favorites.values())})
    
    elif request.method == 'POST':
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        if FavoriteProduct.objects.filter(user=request.user, product=product).exists():
            return Response({'error': 'Product already in favorites'}, status=status.HTTP_400_BAD_REQUEST)
        
        favorite = FavoriteProduct.objects.create(user=request.user, product=product)
        serializer = FavoriteProductSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

