from django.shortcuts import render

#appimport
from .models import *
from .serializers import *
##restframework imports
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response



class GetGrades(APIView):

    authentication_classes=[]
    permission_classes=[]

    def get(self,format=None):
        grades=Grades.objects.all()
        gradesSeralize=GradesSerailizer(grades,many=True)
        return Response(data=gradesSeralize.data,status=status.HTTP_200_OK)

class CreateGrades(APIView):

    authentication_classes=[]
    permission_classes=[]

    def post(self,format=None):
        data=self.request.data
        class_name=data.get("class",None)
        section_name=data.get("section",None)
        validate_arr=["",None]
        if class_name in validate_arr or section_name in validate_arr:
            return Response(data={
                "message":"Provide valid data"
            },status=status.HTTP_400_BAD_REQUEST)
        exist_grades=Grades.objects.filter(name=class_name)
        if exist_grades.exists():
            current_grade=exist_grades[0]
            if current_grade.section==None:
                current_grade.section=[section_name]
            else:
                current_grade.section.append(section_name)
            current_grade.save()
        else:
            current_grade=Grades.objects.create(name=class_name,section=[section_name])
        return Response({
            "message":"Data added successfully",
            "data":GradesSerailizer(current_grade).data
        },status=status.HTTP_200_OK)
    
class CreateStudent(APIView):
    authentication_classes=[]
    permission_classes=[]

    def post(self,format=None):
        data=self.request.data
        name=data.get("name",None)
        grade=data.get("grade",None)
        section=data.get("section",None)
        usn=data.get("usn",None)

        validate_arr=[None,""]
        if name in validate_arr or grade in validate_arr or section in validate_arr or usn in validate_arr:
            return Response({
                "message":"Please provide proper data"
            },status=status.HTTP_400_BAD_REQUEST)
        new_student=Student.objects.create(name=name,grade=grade,section=section,usn=usn)
        return Response({
            "message":"Student Created",
            "data":StudentSerializer(new_student).data
        },status=status.HTTP_200_OK)
        
        
class CreateSubject(APIView):

    authentication_classes=[]
    permission_classes=[]

    def post(self,format=None):
       
        data=self.request.data
        grade=data.get("grade",None)
        subject=data.get("subject",None)
        subject_code=data.get("subject_code",None)
       
        validate_arr=[None,""]
        
        if grade in validate_arr or subject in validate_arr or subject_code in validate_arr:
            return Response({
                "message":f"Please provide proper data"
            },status=status.HTTP_400_BAD_REQUEST)
        
        try:
            gradeInstance=Grades.objects.get(name=grade)
        except Grades.DoesNotExist:
            return Response({
                "message":"Grade not present..Proved valid grade"
            },status=status.HTTP_400_BAD_REQUEST)

        subjectInstance=Subject.objects.create(name=subject,grade=gradeInstance,subject_code=subject_code)
        return Response({
            "message":"Subject created Successfully"
        },status=status.HTTP_200_OK)

class CreateTheme(APIView):

    authentication_classes=[]
    permission_classes=[]

    def post(self,format=None):
        data=self.request.data
        grade=data.get("grade",None)
        name=data.get("name",None)
        centralidea=data.get("centralidea",None)
        lineofinquiry=data.get("lineofinquiry",None)
        validate_arr=[None,""]
        
        if grade in validate_arr or name in validate_arr or centralidea in validate_arr or lineofinquiry in validate_arr:
            return Response({
                "message":f"Please provide proper data"
            },status=status.HTTP_400_BAD_REQUEST)

        try:
            gradeInstance=Grades.objects.get(name=grade)
        except Grades.DoesNotExist:
            return Response({
                "message":"Grade not present..Proved valid grade"
            },status=status.HTTP_400_BAD_REQUEST)

        themeInstance=Theme.objects.create(grade=gradeInstance,name=name,centralidea=centralidea,lineofinquiry=lineofinquiry)
        return Response({
            "message":"Subject created Successfully"
        },status=status.HTTP_200_OK)