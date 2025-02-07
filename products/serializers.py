from rest_framework import serializers
from products.models import Review, Product, Cart, ProductTag, FavoriteProduct

from users.models import User

class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['product_id', 'content', 'rating']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data.pop('product_id'))
        user = self.context['request'].user
        return Review.objects.create(product=product, user=user, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        exclude = ['created_at', 'updated_at', 'tags'] 
        model = Product

class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['user', 'products']

#eseigi vamowmebt arsebobs tu ara produqti ofc
    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value
    
    #rom quantity aris dadebiti mteli rixcvi
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value

    

class ProductTagSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = ProductTag
        fields = ['id', 'name', 'products']


    #aqac vamowmebt producti tu arsebobs
    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value
    
    #tag name unikalurobas amowmebs
    def validate_tag_name(self, value):
        product_id = self.initial_data.get('product')
        if ProductTag.objects.filter(product_id=product_id, tag_name=value).exists():
            raise serializers.ValidationError("Tag name must be unique for this product.")
        return value
    
class FavoriteProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = FavoriteProduct
        fields = ['id', 'user', 'products']

    #aqac vamowmebt producti tu arsebobs
    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    #rom user uewveli arsebobs
    def validate_user(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("User  does not exist.")
        return value

#mokled wina davaleba rac avtvirte dzaan didi nawili googlis mixedvit vqeni da viewebic gadavakete exa 
#(amjerad serioznad chemit, uket gavige es modelserializerebi da ramerumeebi)
#:D