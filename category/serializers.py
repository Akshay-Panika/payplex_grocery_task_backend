from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    # ✅ For write (create/update)
    category_image = serializers.ImageField(required=False, allow_null=True, write_only=True)
    
    # ✅ For read — returns full Cloudinary URL
    category_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image', 'category_image_url', 'created_at']

    def get_category_image_url(self, obj):
        if obj.category_image:
            return obj.category_image.url  # Cloudinary gives full https:// URL
        return None