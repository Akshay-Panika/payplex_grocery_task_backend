from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer


class CreateOrderView(APIView):

    def post(self, request, user_id):
        data = request.data.copy()
        data['user_id'] = user_id

        serializer = OrderSerializer(data=data)

        if serializer.is_valid():
            order = serializer.save()

            return Response({
                "status": True,
                "message": "Order created",
                "order_id": order.order_id,
                "data": OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

class OrderListView(APIView):

    def get(self, request, user_id):
        orders = Order.objects.filter(user_id=user_id).order_by('-id')

        serializer = OrderSerializer(orders, many=True)

        return Response({
            "status": True,
            "count": orders.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
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