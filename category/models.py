from django.db import models
from cloudinary.models import CloudinaryField

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    category_image = CloudinaryField('image', folder='category')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name