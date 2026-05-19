from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from rest_framework import status


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


class DeleteOrderView(APIView):

    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({
                "status": True,
                "message": "Order deleted successfully"
            }, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({
                "status": False,
                "message": "Order not found"
            }, status=status.HTTP_404_NOT_FOUND)


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