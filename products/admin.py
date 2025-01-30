from django.contrib import admin
from .models import Product, Review, ProductsTag, Cart, FavoriteProduct, ProductImage

admin.site.register(Review)
admin.site.register(ProductsTag)
admin.site.register(Cart)
admin.site.register(FavoriteProduct)
admin.site.register(ProductImage)

class ImageInLine(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInLine]