from django.contrib import admin
from .models import Category, Product, ProductImage

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'parent', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('is_active', 'created_at', 'parent')

# Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'stock', 'is_available', 'is_featured')
    list_filter = ('is_available', 'is_featured', 'category', 'created_at')
    search_fields = ('name', 'brand', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
