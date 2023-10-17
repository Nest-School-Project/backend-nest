from .models import *

from rest_framework.serializers import ModelSerializer

class GradesSerailizer(ModelSerializer):

    class Meta:
        model=Grades
        fields='__all__'

class StudentSerializer(ModelSerializer):

    class Meta:
        model=Student
        fields='__all__'

class AssessmentSerializer(ModelSerializer):

    class Meta:
        model=Assessment
        fields="__all__"
        depth=1

class ThemeSerializer(ModelSerializer):

    class Meta:
        model=Theme
        fields="__all__"
        depth=1

class SubjectSerializer(ModelSerializer):
    class Meta:
        model=Subject
        fields="__all__"
        depth=1

class MarkEntrySerializer(ModelSerializer):

    class Meta:
        model=MarkEntry
        fields="__all__"
        depth=1