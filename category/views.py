from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Category
from .serializers import CategorySerializer

class CategoryCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = CategorySerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Category created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
     
    
class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all().order_by('-id')
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response({
            "status": True,
            "data": serializer.data
        })


class CategoryUpdateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"status": False, "message": "Category not found"}, status=404)

        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Category updated successfully",
                "data": serializer.data
            })

        return Response({"status": False, "errors": serializer.errors}, status=400)


class CategoryDeleteView(APIView):
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"status": False, "message": "Category not found"}, status=404)

        category.delete()
        return Response({
            "status": True,
            "message": "Category deleted successfully"
        })