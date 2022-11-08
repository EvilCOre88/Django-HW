from rest_framework import serializers

from .models import Course, Places
from django.conf import settings
from django.core.exceptions import ValidationError

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

class PlacesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Places
        fields = ('id', 'course', 'student')

    def validate(self, val):
        course = val['course']
        places = Places.objects.filter(course=course)
        if len(places) >= settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(f'Ошибка: Превышено максимальное ({settings.MAX_STUDENTS_PER_COURSE}) количество'
                                  f'студентов на курс')
        return val