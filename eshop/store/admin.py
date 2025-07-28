from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'parent', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'stock', 'is_available', 'is_featured')
    list_filter = ('is_available', 'is_featured', 'category')
    search_fields = ('name', 'brand', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
