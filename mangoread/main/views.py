from users.models import Profile

import django_filters
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from main.models import Manga, Review
from main.serializers import MangaDetailSerializer, MangaListSerializer, ReviewCreateSerializer, ReviewSerializer


class CharFilterInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class MangaFilter(django_filters.FilterSet):
    genre = CharFilterInFilter(field_name='genre__name', lookup_expr='in', distinct=True)
    year = django_filters.RangeFilter()

    class Meta:
        model = Manga
        fields = ['genre', 'year']


# Create your views here.
class MangaPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 12


class MangaListAPIView(ReadOnlyModelViewSet):
    serializer_class = MangaListSerializer
    queryset = Manga.objects.all()
    pagination_class = MangaPagination
    filterset_class = MangaFilter
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


class MangaDetailAPIView(ReadOnlyModelViewSet):
    queryset = Manga.objects.filter()
    serializer_class = MangaDetailSerializer


class ReviewAPIView(ModelViewSet):
    serializer_class = ReviewCreateSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get_manga(self):
        obj = get_object_or_404(Manga, pk=self.kwargs.get('pk'))
        return obj

    def list(self, request, *args, **kwargs):
        queryset = Review.objects.filter(manga=self.get_manga())
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(user=profile)

        return Response({"post": serializer.data})

    def get_queryset(self, pk=None):
        return Review.objects.all()
