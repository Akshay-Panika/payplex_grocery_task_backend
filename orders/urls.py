from django.urls import path
from .views import CreateOrderView, OrderListView, DeleteOrderView

urlpatterns = [
    path('create/<int:user_id>/', CreateOrderView.as_view()),
    path('list/<int:user_id>/', OrderListView.as_view()),
    path('delete/<int:pk>/', DeleteOrderView.as_view()),
]