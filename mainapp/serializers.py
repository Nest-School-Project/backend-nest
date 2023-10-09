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

