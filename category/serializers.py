from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image', 'created_at']

    # Moves the case-insensitive validation logic out of the view and into the serializer
    def validate_category_name(self, value):
        # On update, exclude the current instance from the duplicate check
        instance = self.instance
        queryset = Category.objects.filter(category_name__iexact=value)
        
        if instance:
            queryset = queryset.exclude(pk=instance.pk)
            
        if queryset.exists():
            raise serializers.ValidationError("Category name already exists")
        return value