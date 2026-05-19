from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, LoginSerializer
from .models import User


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response({
                "status": True,
                "message": "User registered successfully",
                "data": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone,
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        errors = {}

        #  check user by email first
        user_obj = User.objects.filter(email=email).first()

        if not user_obj:
            errors["email"] = "Invalid email"

        #  check password only if user exists
        if user_obj and not user_obj.check_password(password):
            errors["password"] = "Invalid password"

        #  if any error
        if errors:
            return Response({
                "status": False,
                "errors": errors
            }, status=status.HTTP_400_BAD_REQUEST)

        #  success login
        return Response({
            "status": True,
            "message": "Login successful",
            "data": {
                "id": user_obj.id,
                "name": user_obj.name,
                "email": user_obj.email,
                "phone": user_obj.phone,
            }
        })

class ForgetPasswordView(APIView):

    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        try:
            user = User.objects.get(email=email)

            # password update
            user.set_password(new_password)
            user.save()

            return Response({
                "status": True,
                "message": "Password updated successfully"
            })

        except User.DoesNotExist:
            return Response({
                "status": False,
                "message": "Invalid email"
            }, status=400)

class UserListView(APIView):

    def get(self, request):
        users = User.objects.all()

        data = [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
            }
            for user in users
        ]

        return Response({
            "status": True,
            "data": data
        })


class UserDetailView(APIView):

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)

            return Response({
                "status": True,
                "data": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone,
                }
            })

        except User.DoesNotExist:
            return Response({
                "status": False,
                "message": "User not found"
            }, status=404)