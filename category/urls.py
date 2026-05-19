from django.urls import path
from .views import (
    CategoryCreateView,
    CategoryListView,
    CategoryUpdateView,
    CategoryDeleteView
)

urlpatterns = [
    path('create/', CategoryCreateView.as_view()),
    path('list/', CategoryListView.as_view()),
    path('update/<int:pk>/', CategoryUpdateView.as_view()),
    path('delete/<int:pk>/', CategoryDeleteView.as_view()),
]