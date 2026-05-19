from decimal import Decimal
from django.db import models
from category.models import Category  

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to='products/', null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_description = models.TextField(blank=True, null=True)
    isOffer = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

    @property
    def discounted_price(self):  
        if self.isOffer:
            return self.product_price * Decimal('0.5')
        return self.product_price