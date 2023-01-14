from django.urls import path
from .views import MangaListAPIView, MangaDetailAPIView, ReviewAPIView

urlpatterns = [
    path('mainpage/', MangaListAPIView.as_view({'get': 'list'})),
    path('<int:pk>/', MangaDetailAPIView.as_view({'get': 'retrieve'})),
    path("<int:pk>/review/", ReviewAPIView.as_view({'get': 'list', 'post': 'create'}))
]
