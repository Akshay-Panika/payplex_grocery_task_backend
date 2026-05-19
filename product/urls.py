from django.urls import path
from .views import ProductListCreateView, ProductDetailView

urlpatterns = [
    path('list/', ProductListCreateView.as_view(), name='product-list-create'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'), 
]