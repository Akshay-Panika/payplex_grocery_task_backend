from django.urls import path
from .views import RegisterView, LoginView, UserListView, UserDetailView, ForgetPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('forget-password/', ForgetPasswordView.as_view()),

    path('users/', UserListView.as_view()),
    path('users/<int:id>/', UserDetailView.as_view()),
]