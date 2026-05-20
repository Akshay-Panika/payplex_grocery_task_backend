from decimal import Decimal
from rest_framework import serializers

from .models import Product
from category.serializers import CategorySerializer

# ✅ image compression import
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


# =========================
# 🔥 IMAGE COMPRESSOR
# =========================
def compress_image(image):
    img = Image.open(image)

    # convert to RGB (fix PNG / WEBP issues)
    if img.mode != "RGB":
        img = img.convert("RGB")

    output = BytesIO()

    # compress quality
    img.save(output, format='JPEG', quality=70, optimize=True)

    output.seek(0)

    return InMemoryUploadedFile(
        output,
        'ImageField',
        image.name,
        'image/jpeg',
        output.getbuffer().nbytes,
        None
    )


# =========================
# 🔥 SERIALIZER
# =========================
class ProductSerializer(serializers.ModelSerializer):

    category_details = CategorySerializer(
        source='category',
        read_only=True
    )

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

    # =========================
    # 🔥 IMAGE VALIDATION + COMPRESS
    # =========================
    def validate_product_image(self, value):
        if value:

            # compress FIRST
            value = compress_image(value)

            # safety check (Cloudinary free limit)
            max_size = 10 * 1024 * 1024  # 10MB

            if value.size > max_size:
                raise serializers.ValidationError(
                    "Image too large even after compression"
                )

        return value

    # =========================
    # 🔥 DISCOUNT LOGIC
    # =========================
    def get_discounted_price(self, obj):
        if obj.isOffer:
            return str(obj.product_price * Decimal('0.5'))
        return str(obj.product_price)

    # =========================
    # 🔥 RESPONSE CLEANUP
    # =========================
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['category_details'] = CategorySerializer(
            instance.category,
            context=self.context
        ).data

        data['product_image'] = (
            instance.product_image.url
            if instance.product_image else None
        )

        return data