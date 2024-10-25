from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    # Display fields
    list_display = ('product_name', 'product_category', 'product_price', 'user', 'created_at')

    # Add filter options
    list_filter = ('product_category', 'user', 'created_at')

    # Add search functionality
    search_fields = ('product_name', 'product_category', 'user__username')

    # Ordering options
    ordering = ('-created_at',)

    # Fields to show links
    list_display_links = ('product_name',)

    # Fields editable directly in the list view
    list_editable = ('product_price',)

admin.site.register(Product, ProductAdmin)
