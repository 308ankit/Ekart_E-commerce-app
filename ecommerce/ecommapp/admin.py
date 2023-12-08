from django.contrib import admin
from ecommapp.models import Products


# Register your models here.

#admin.site.register(Products)

class ProductsAdmin(admin.ModelAdmin):
    list_display=['id','name','cat','price','is_active','pimage']
    list_filter=['cat','is_active']
admin.site.register(Products,ProductsAdmin)
