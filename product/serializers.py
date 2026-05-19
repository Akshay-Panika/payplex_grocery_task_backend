from rest_framework import serializers
from .models import Product
from category.models import Category
from category.serializers import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'category',         
            'category_details', 
            'product_name',
            'product_image', 
            'product_price',
            'offer_price',
            'product_description',
            'isOffer',
            'created_at'
        ]

    def validate(self, data):
        is_offer_raw = data.get('isOffer')
        
        if isinstance(is_offer_raw, str):
            if is_offer_raw.lower() == 'false':
                data['isOffer'] = False
            elif is_offer_raw.lower() == 'true':
                data['isOffer'] = True

        is_offer = data.get('isOffer', False)
        offer_price = data.get('offer_price')

        if is_offer and (offer_price is None or offer_price == ''):
            raise serializers.ValidationError({
                "offer_price": "Offer price is required when isOffer is set to True."
            })

        if not is_offer:
            data['offer_price'] = None

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category_details'] = CategorySerializer(instance.category, context=self.context).data
        return representation