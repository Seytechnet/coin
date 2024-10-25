from django.db import models
from django.contrib.auth.models import User
from django.utils.formats import number_format

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('home_kitchen', 'Home & Kitchen'),
        ('health_beauty', 'Health & Beauty'),
        ('jewelry_accessories', 'Jewelry & Accessories'),
        ('apparel_fashion', 'Apparel & Fashion'),
        ('food', 'Food'),
        ('gadgets_computers', 'Gadgets & Computers'),
    ]

    LOCATION_CHOICES = [
        ('school hostel', 'School Hostel'),
        ('gate', 'Gate'),
        ('agbede', 'Agbede'),
        ('kofesu', 'Kofesu'),
        ('harmony', 'Harmony'),
        ('accord', 'Accord'),
        ('zoo', 'Zoo'),
        ('oluwo', 'Oluwo'),
        ('isolu', 'Isolu'),
        ('camp', 'Camp'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    product_image_url = models.URLField(max_length=500, blank=True, null=True)  # Updated to store ImgBB URL
    product_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)  
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name if self.product_name else 'Unnamed Product'

    def formatted_price(self):
        if self.product_price:
            return f"{int(self.product_price):,}"  # Format the price with commas
        return "Price Not Available"
