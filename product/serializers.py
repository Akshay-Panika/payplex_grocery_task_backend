from decimal import Decimal
from rest_framework import serializers
from .models import Product
from category.serializers import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    discounted_price = serializers.SerializerMethodField()  

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'category_details',
            'product_name',
            'product_image',
            'product_price',
            'isOffer',          
            'discounted_price', 
            'product_description',
            'created_at'
        ]

    def get_discounted_price(self, obj):  
        if obj.isOffer:
            return float(obj.product_price * Decimal('0.5'))
        return float(obj.product_price)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category_details'] = CategorySerializer(
            instance.category,
            context=self.context
        ).data
        return representation