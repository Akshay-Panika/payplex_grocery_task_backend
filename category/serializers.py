from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image', 'created_at']

    def validate_category_name(self, value):
        instance = self.instance

        queryset = Category.objects.filter(category_name__iexact=value)

        if instance:
            queryset = queryset.exclude(pk=instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Category name already exists")

        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['category_image'] = (
            instance.category_image.url
            if instance.category_image else None
        )

        return representation