from django.contrib import admin
from .models import Product, Favourite

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
   list_display = ('id', 'name', 'price', 'site')

class FavouriteAdmin(admin.ModelAdmin):
   list_display = ('user', 'product')

admin.site.register(Product, ProductAdmin)
admin.site.register(Favourite, FavouriteAdmin)