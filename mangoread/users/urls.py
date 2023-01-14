from django.urls import path
from .views import RegisterAPIView, LoginAPIView, RestorePasswordAPIView, ChangePasswordView, ProfileView, UserViewSet

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('restore-password/', RestorePasswordAPIView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('users-list/', UserViewSet.as_view({'get': 'list'}))
]
