from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser 

from .models import Product
from .serializers import ProductSerializer


class ProductListCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(
            products,
            many=True,
            context={'request': request}
        )

        return Response({
            "status": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": True,
                "message": "Product created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)

        if not product:
            return Response({
                "status": False,
                "message": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(
            product,
            context={'request': request}
        )

        return Response({
            "status": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = self.get_object(pk)

        if not product:
            return Response({
                "status": False,
                "message": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": True,
                "message": "Product updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)

        if not product:
            return Response({
                "status": False,
                "message": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)

        product.delete()

        return Response({
            "status": True,
            "message": "Product deleted successfully"
        }, status=status.HTTP_200_OK)