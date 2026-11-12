from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "is_available", "updated_at"]
    list_filter = ["category", "is_available"]
    search_fields = ["name"]
    list_editable = ["price", "is_available"]
