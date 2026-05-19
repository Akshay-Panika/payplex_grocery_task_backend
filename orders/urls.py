from django.urls import path
from .views import CreateOrderView, OrderListView,DeleteOrderView

urlpatterns = [
    path('create/', CreateOrderView.as_view()),
    path('list/', OrderListView.as_view()),
    path('delete/<int:pk>/', DeleteOrderView.as_view()),

]