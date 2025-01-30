from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from products.serializers import ProductSerializer

@api_view(['GET', 'POST'])
def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        products_list = []
        
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'currency': product.currency,
                'quantity': product.quantity
            }
            products_list.append(product_data)
            
        return Response({'products': products_list})
    elif request.method == 'POST':
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            created_product = Product.objects.create(
                name=data.get('name'),
                description=data.get('description'),
                price=data.get('price'),
                currency=data.get('currency', 'gel'),
                quantity=data.get('quantity')
            )
            return Response({'id': created_product.id}, status=status.HTTP_201_CREATED)
        else:
            return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))
