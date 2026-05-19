from django.urls import path
from .views import CreateOrderView, OrderListView

urlpatterns = [
    path('create/', CreateOrderView.as_view()),
    path('list/', OrderListView.as_view()),
]