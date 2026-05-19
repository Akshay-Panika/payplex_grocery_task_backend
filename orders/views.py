from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer


# CREATE ORDER
class CreateOrderView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            order = serializer.save()

            return Response({
                "status": True,
                "message": "Order created",
                "order_id": order.order_id,
                "data": OrderSerializer(order).data
            })

        return Response({
            "status": False,
            "errors": serializer.errors
        })


# GET ALL ORDERS
class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.all().order_by('-id')
        serializer = OrderSerializer(orders, many=True)

        return Response({
            "status": True,
            "count": orders.count(),
            "data": serializer.data
        })