from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .filters import CourseFilter
from .models import Course, Places
from .serializers import CourseSerializer, PlacesSerializer


class CoursesViewSet(ModelViewSet):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = CourseFilter

class PlacesViewSet(ModelViewSet):
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer