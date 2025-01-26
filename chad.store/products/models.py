from django.db import models
from config.model_utils.models import TimeStampModel
from products.choices import Currency
from django.core.validators import MaxValueValidator

class Product(TimeStampModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=255, choices=Currency.choices, default=Currency.GEL)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.price} {self.currency} (quantity: {self.quantity})"
    
class Review(TimeStampModel):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    
    def __str__(self):
        return f"{self.product.name}: rated by {self.user} - {self.rating}/5"

class ProductsTag(TimeStampModel):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField('products.Product', related_name='produc_tags')

    def __str__(self):
        return self.name
    
class Cart(TimeStampModel):
    products = models.ManyToManyField('products.Product', related_name = 'carts')
    user = models.OneToOneField('users.User', related_name='cart', on_delete=models.CASCADE) 
    
class FavoriteProduct(TimeStampModel):
    product = models.ForeignKey('products.Product', related_name='favorite_products', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='favorite_product', on_delete=models.SET_NULL, null=True, blank=True)
    
class ProductImage(TimeStampModel):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey('products.Product', related_name='images', on_delete=models.CASCADE)
    
    
    