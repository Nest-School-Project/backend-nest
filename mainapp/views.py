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
class GetGradeDetails(APIView):

    authentication_classes=[]
    permission_classes=[]

    def get(self,format=None):
        grade=self.request.GET.get("grade")
        try:
            gradeInstace=Grades.objects.get(name=grade)
        except Grades.DoesNotExist:
            return Response({
                "message":"Grade is not present"
            },status=status.HTTP_400_BAD_REQUEST)
        gradesSerialized=GradesSerailizer(gradeInstace)
        return Response(data=gradesSerialized.data,status=status.HTTP_200_OK)
    
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
            "message":"Theme created Successfully"
        },status=status.HTTP_200_OK)

class CreateAssessment(APIView):

    authentication_classes=[]
    permission_classes=[]

    def post(self,format=None):
        data=self.request.data
        assessmentType=data.get("assessment_type",None)  ## FA or SA
        assessmentName=data.get("assessment_name",None)
        assessmentFor=data.get("assessment_for",None)    ## UOI or subject
        theme=data.get("theme",None)
        grade=data.get("grade",None)

        validate_arr=[None,""]

        if assessmentType in validate_arr or assessmentName in validate_arr or assessmentFor in validate_arr or grade in validate_arr:
            return Response({
                "message":"Please provide all data"
            },status=status.HTTP_400_BAD_REQUEST)
        if assessmentFor=="UOI":
            try:
                gradeInstance=Grades.objects.get(name=grade)
            except Grades.DoesNotExist:
                return Response({
                    "message":"Grade does not exist"
                },status=status.HTTP_400_BAD_REQUEST)
            try:
                themeInstance=Theme.objects.get(name=theme)
            except Theme.DoesNotExist:
                return Response({
                    "message":"Theme data is not present"
                },status=status.HTTP_400_BAD_REQUEST)

            assessmentInstance=Assessment.objects.create(assessmentType=assessmentType,assessmentName=assessmentName,assessmentFor=assessmentFor,theme=themeInstance,grade=gradeInstance)
        else:
            try:
                gradeInstance=Grades.objects.get(name=grade)
            except Grades.DoesNotExist:
                return Response({
                    "message":"Grade does not exist"
                },status=status.HTTP_400_BAD_REQUEST)

            subjects=Subject.objects.filter(grade=gradeInstance)
            assessmentInstance=Assessment.objects.create(assessmentType=assessmentType,assessmentName=assessmentName,assessmentFor=assessmentFor,grade=gradeInstance)
            for i in subjects:
                assessmentInstance.subject.add(i)
                assessmentInstance.save()
        assessmentSerializer=AssessmentSerializer(assessmentInstance)        
        return Response({
            "message":"Assessment Created Successfully",
            "data":assessmentSerializer.data
        },status=status.HTTP_200_OK)

class GetStudentList(APIView):
    authentication_classes=[]
    permission_classes=[]

    def get(self,format=None):
        grade=self.request.GET.get("grade")
        

        valid_arr=[None,""]

        if grade in valid_arr:
            return Response({
                "message":"Provide proper data"
            },status=status.HTTP_400_BAD_REQUEST)

        else:
            students=Student.objects.filter(grade=grade)
            studentsSerializer=StudentSerializer(students,many=True)

        return Response({
            "data":studentsSerializer.data
        },status=status.HTTP_200_OK)


class UpdateMarks(APIView):

    authentication_classes=[]
    permission_classes=[]

    def post(self,format=None):
        data=self.request.data
        grade=data.get("grade",None)
        type_assessment=data.get("type",None)
        assessment_for=data.get("assessment_for",None)
        try:
            gradeInstance=Grades.objects.get(name=grade)
        except Grades.DoesNotExist:
            return Response({
                "message":"Grade does not exist"
            },status=status.HTTP_400_BAD_REQUEST)
        if assessment_for=="theme":
            theme=data.get("theme",None)
            try:
                themeInstance=Theme.objects.get(id=theme)
            except Theme.DoesNotExist:
                return Response({
                    "message":"Theme does not exists"
                },status=status.HTTP_200_OK)
            marks=data.get("marks",None)
            for i in marks:
                try:
                    studentInstance=Student.objects.get(usn=i)
                except Student.DoesNotExist:
                    return Response({
                        "message":"Student does not exists"
                    },status=status.HTTP_400_BAD_REQUEST)
                for j in marks[i]:
                    try:
                        assessmentInstance=Assessment.objects.get(id=j)
                    except Assessment.DoesNotExist:
                        return Response({
                            "message":"Assessment does not exists"
                        },status=status.HTTP_400_BAD_REQUEST)
                    markEntryInstance=MarkEntry.objects.get_or_create(assessment=assessmentInstance,grade=gradeInstance,student=studentInstance,theme=themeInstance)[0]
                    markEntryInstance.marks=marks[i][j]
                    markEntryInstance.save()
        else:
            subject=data.get("subject",None)
            try:
                subjectInstance=Subject.objects.get(id=subject)
            except Subject.DoesNotExist:
                return Response({
                    "message":"subject does not exist"
                },status=status.HTTP_400_BAD_REQUEST)
            marks=data.get("marks",None)
            for i in marks:
                try:
                    studentInstance=Student.objects.get(usn=i)
                except Student.DoesNotExist:
                    return Response({
                        "message":"Student does not exists"
                    },status=status.HTTP_400_BAD_REQUEST)
                for j in marks[i]:
                    try:
                        assessmentInstance=Assessment.objects.get(id=j)
                    except Assessment.DoesNotExist:
                        return Response({
                            "message":"Assessment does not exists"
                        },status=status.HTTP_400_BAD_REQUEST)
                    markEntryInstance=MarkEntry.objects.get_or_create(assessment=assessmentInstance,grade=gradeInstance,student=studentInstance,subject=subjectInstance)[0]
                    markEntryInstance.marks=marks[i][j]
                    markEntryInstance.save()
            return Response({
                "message":"Mark updated Successfully"
            },status=status.HTTP_200_OK)

class GetThemes(APIView):

    authentication_classes=[]
    permission_classes=[]

    def get(self,format=None):
        grade=self.request.GET.get("grade",None)
        if grade==None:
            themes=Theme.objects.all()
            themesSerialized=ThemeSerializer(themes,many=True)
            return Response(themesSerialized.data,status=status.HTTP_200_OK)
        else:
            try:
                gradeInstance=Grades.objects.get(name=grade)
            except Grades.DoesNotExist:
                return Response({
                    "message":"Invalid data"
                },status=status.HTTP_400_BAD_REQUEST)
            theme=Theme.objects.filter(grade=gradeInstance)
            themesSerialized=ThemeSerializer(theme,many=True)
            return Response(themesSerialized.data,status=status.HTTP_200_OK)

class GetSubjects(APIView):

    authentication_classes=[]
    permission_classes=[]

    def get(self,format=None):
        grade=self.request.GET.get("grade",None)
        if grade==None:
            subjects=Subject.objects.all()
            subjectserialized=SubjectSerializer(subjects,many=True)
            return Response(subjectserialized.data,status=status.HTTP_200_OK)
        else:
            try:
                gradeInstance=Grades.objects.get(name=grade)
            except Grades.DoesNotExist:
                return Response({
                    "message":"Invalid data"
                },status=status.HTTP_400_BAD_REQUEST)

            subjects=Subject.objects.filter(grade=gradeInstance)
            subjectserialized=SubjectSerializer(subjects,many=True)
            return Response(subjectserialized.data,status=status.HTTP_200_OK)

class GetThemeMarks(APIView):

    authentication_classes=[]
    permission_classes=[]

    def get(self,format=None):
        grade=self.request.GET.get("grade",None)
        section=self.request.GET.get("section",None)
        theme=self.request.GET.get("theme",None)

        try:
            gradeInstance=Grades.objects.get(name=grade)
        except Grades.DoesNotExist:
            return Response({
                "message":"Grade does not exists"
            },status=status.HTTP_400_BAD_REQUEST)

        try:
            themeInstance=Theme.objects.get(name=theme,grade=gradeInstance)
        except Theme.DoesNotExist:
            return Response({
                "message":"Theme does not exists"
            },status=status.HTTP_400_BAD_REQUEST)

        students=Student.objects.filter(grade=grade,section=section)

        marks_instance=MarkEntry.objects.filter(grade=gradeInstance,theme=themeInstance,student__in=students)
        markInstanceSerialized=MarkEntrySerializer(marks_instance,many=True)

        return Response(markInstanceSerialized.data,status=status.HTTP_200_OK)

class GetAssessmentList(APIView):

    authentication_classes=[]
    permission_classes=[]

    def get(self,format=None):
        grade=self.request.GET.get("grade",None)
        assessment_type=self.request.GET.get("type",None)
        try:
            gradeInstance=Grades.objects.get(name=grade)
        except Grades.DoesNotExist:
            return Response({
                "message":"Invalid data"
            },status=status.HTTP_400_BAD_REQUEST)

        if assessment_type==None:
            assessments=Assessment.objects.filter(grade=gradeInstance)
        else:
            assessments=Assessment.objects.filter(grade=gradeInstance,assessmentType=assessment_type)
        
        assessmentSerialized=AssessmentSerializer(assessments,many=True)
        return Response(assessmentSerialized.data,status=status.HTTP_200_OK)

class UpdateThemeMarks(APIView):

    authentication_classes=[]
    permission_classes=[]

    def post(self,format=None):
        data=self.request.data.get("data","df")
        
        try:
            grade_instance=Grades.objects.get(name=data['class_name'])        

        except Grades.DoesNotExist:
            return Response({
                "message":"Grade does not exist"
            },status=status.HTTP_400_BAD_REQUEST)
        
        try:
            theme_instance=Theme.objects.get(name=data['theme_name'],grade=grade_instance)
        except Theme.DoesNotExist:
            return Response(
                {
                "message":"Invalid theme"},
                status=status.HTTP_400_BAD_REQUEST
                )

        
        
        for i in data['students']:
            try:
                student_instance=Student.objects.get(usn=i['usn'])
            except Student.DoesNotExist:
                continue

            for j in data['marks'][i['usn']]["FA"]:
                try:
                    assessment_instance=Assessment.objects.get(assessmentName=j,theme=theme_instance,grade=grade_instance,assessmentFor="UOI",assessmentType="FA")
                except Assessment.DoesNotExist:
                    return Response(
                        {
                            "message":"Does not exist"
                        },status=status.HTTP_400_BAD_REQUEST
                    )
                marksInstance=MarkEntry.objects.get_or_create(assessment=assessment_instance,grade=grade_instance,student=student_instance,theme=theme_instance)[0]
                marksInstance.marks=data['marks'][i['usn']]["FA"][j]
                marksInstance.save()
            for j in data['marks'][i['usn']]["SA"]:
                try:
                    assessment_instance=Assessment.objects.get(assessmentName=j,theme=theme_instance,grade=grade_instance,assessmentFor="UOI",assessmentType="SA")
                except Assessment.DoesNotExist:
                    return Response(
                        {
                            "message":"Does not exist"
                        },status=status.HTTP_400_BAD_REQUEST
                    )
                marksInstance=MarkEntry.objects.get_or_create(assessment=assessment_instance,grade=grade_instance,student=student_instance,theme=theme_instance)[0]
                marksInstance.marks=data['marks'][i['usn']]["SA"][j]
                marksInstance.save()
        
        return Response({
            "message":"Updated Successfully"
        },status=status.HTTP_200_OK)


class GetSubjectMarks(APIView):

    authentication_classes=[]
    permission_classes=[]

    def get(self,format=None):
        grade=self.request.GET.get("grade",None)
        subject=self.request.GET.get("subject",None)
        section=self.request.GET.get("section",None)
        try:
            gradeInstance=Grades.objects.get(name=grade)
        except Grades.DoesNotExist:
            return Response({
                "message":"Grade does not exists"
            },status=status.HTTP_400_BAD_REQUEST)

        try:
            subjectInstance=Subject.objects.get(name=subject,grade=gradeInstance)
        except Subject.DoesNotExist:
            return Response({
                "message":"Subject does not exists"
            },status=status.HTTP_400_BAD_REQUEST)

        students=Student.objects.filter(grade=grade,section=section)

        marks_instance=MarkEntry.objects.filter(grade=gradeInstance,subject_code=subjectInstance,student__in=students)
        markInstanceSerialized=MarkEntrySerializer(marks_instance,many=True)

        return Response(markInstanceSerialized.data,status=status.HTTP_200_OK)

class UpdateSubjectMarks(APIView):

    authentication_classes=[]
    permission_classes=[]

    def post(self,format=None):
        data=self.request.data.get("data","df")
        try:
            grade_instance=Grades.objects.get(name=data['class_name'])        

        except Grades.DoesNotExist:
            return Response({
                "message":"Grade does not exist"
            },status=status.HTTP_400_BAD_REQUEST)
        
        try:
            subject_instance=Subject.objects.get(name=data['subject_name'],grade=grade_instance)
        except Subject.DoesNotExist:
            return Response(
                {
                "message":"Invalid theme"},
                status=status.HTTP_400_BAD_REQUEST
                )

        
        
        for i in data['students']:
            try:
                student_instance=Student.objects.get(usn=i['usn'])
            except Student.DoesNotExist:
                continue

            for j in data['marks'][i['usn']]["FA"]:
                try:
                    assessment_instance=Assessment.objects.get(assessmentName=j,grade=grade_instance,assessmentFor="subject",assessmentType="FA")
                except Assessment.DoesNotExist:
                    return Response(
                        {
                            "message":"Does not exist"
                        },status=status.HTTP_400_BAD_REQUEST
                    )
                marksInstance=MarkEntry.objects.get_or_create(assessment=assessment_instance,grade=grade_instance,student=student_instance,subject_code=subject_instance)[0]
                marksInstance.marks=data['marks'][i['usn']]["FA"][j]
                marksInstance.save()
            for j in data['marks'][i['usn']]["SA"]:
                try:
                    assessment_instance=Assessment.objects.get(assessmentName=j,grade=grade_instance,assessmentFor="subject",assessmentType="SA")
                except Assessment.DoesNotExist:
                    return Response(
                        {
                            "message":"Does not exist"
                        },status=status.HTTP_400_BAD_REQUEST
                    )
                marksInstance=MarkEntry.objects.get_or_create(assessment=assessment_instance,grade=grade_instance,student=student_instance,subject_code=subject_instance)[0]
                marksInstance.marks=data['marks'][i['usn']]["SA"][j]
                marksInstance.save()
        
        return Response({
            "message":"Updated Successfully"
        },status=status.HTTP_200_OK)
    
class GetIndividualFaAnalysis(APIView):

    authentication_classes=[]
    permission_classes=[]

    def get(self,format=None):
        usn=self.request.GET.get("usn",None)
        try:
            student_instance=Student.objects.get(usn=usn)
        except Student.DoesNotExist:
            return Response({
                "message":"Students does not exists"
            },status=status.HTTP_400_BAD_REQUEST)

        try:
            grade_instance=Grades.objects.get(name=student_instance.grade)
        except Grades.DoesNotExist:
            return Response({
                "message":"Grade does not exist"
            },status=status.HTTP_400_BAD_REQUEST)

        themes=Theme.objects.filter(grade=grade_instance)
        subjects=Subject.objects.filter(grade=grade_instance)
        response_json={
            "student_name":student_instance.name,
            "student_usn":student_instance.usn,
            "student_grade":student_instance.grade,
            "student_section":student_instance.section,
            "themes":[],
            "subjects":[],
        }
        for i in themes:
            marks=[]
            assessments=Assessment.objects.filter(assessmentType="FA",assessmentFor="UOI",theme=i,grade=grade_instance)
            for j in assessments:
                try:
                    marks_instance=MarkEntry.objects.get(assessment=j,grade=grade_instance,theme=i,student=student_instance)
                except:
                    marks.append({
                        "name":j.assessmentName,
                        "mark":{
                            "c1":"NA",
                            "c2":"NA",
                        }
                    })
                    continue
                marks.append({
                    "name":j.assessmentName,
                    "mark":marks_instance.marks
                })
            response_json["themes"].append({
                "name":i.name,
                "marks":marks
            })
        for i in subjects:
            marks=[]
            assessments=Assessment.objects.filter(assessmentType="FA",assessmentFor="subject",grade=grade_instance)
            for j in assessments:
                try:
                    marks_instance=MarkEntry.objects.get(assessment=j,grade=grade_instance,subject_code=i,student=student_instance)
                except MarkEntry.DoesNotExist:
                    marks.append({
                        "name":j.assessmentName,
                        "mark":{
                            "c1":"NA",
                            "c2":"NA",
                        }
                    })
                    continue

                marks.append({
                    "name":j.assessmentName,
                    "mark":marks_instance.marks
                })
            response_json["subjects"].append({
                "name":i.name,
                "marks":marks
            })

        return Response(response_json,status=status.HTTP_200_OK)

class GetIndividualSaAnalysis(APIView):



    authentication_classes=[]
    permission_classes=[]

    def get(self,format=None):
        usn=self.request.GET.get("usn",None)
        try:
            student_instance=Student.objects.get(usn=usn)
        except Student.DoesNotExist:
            return Response({
                "message":"Students does not exists"
            },status=status.HTTP_400_BAD_REQUEST)

        try:
            grade_instance=Grades.objects.get(name=student_instance.grade)
        except Grades.DoesNotExist:
            return Response({
                "message":"Grade does not exist"
            },status=status.HTTP_400_BAD_REQUEST)

        themes=Theme.objects.filter(grade=grade_instance)
        subjects=Subject.objects.filter(grade=grade_instance)

        response_json={
            "student_name":student_instance.name,
            "student_usn":student_instance.usn,
            "student_grade":student_instance.grade,
            "student_section":student_instance.section,
            "themes":[],
            "subjects":[],
        }

        for i in themes:
            marks=[]
            assessment=Assessment.objects.filter(assessmentType="SA",assessmentFor="UOI",theme=i,grade=grade_instance)
            for j in assessment:
                try:
                    marks_instance=MarkEntry.objects.get(assessment=j,grade=grade_instance,theme=i,student=student_instance)
                except:
                    marks.append({
                        "name":j.assessmentName,
                        "mark":{
                            "c1":"NA",
                            "c2":"NA",
                            "c3":"NA",
                            "c4":"NA",
                            "c5":"NA",
                        }
                    })
                    continue
                marks.append({
                    "name":j.assessmentName,
                    "mark":marks_instance.marks
                })
            response_json["themes"].append({
                "name":i.name,
                "marks":marks
            })
        for i in subjects:
            marks=[]
            assessments=Assessment.objects.filter(assessmentType="SA",assessmentFor="subject",grade=grade_instance)
            for j in assessments:
                try:
                    marks_instance=MarkEntry.objects.get(assessment=j,grade=grade_instance,subject_code=i,student=student_instance)
                except MarkEntry.DoesNotExist:
                    marks.append({
                        "name":j.assessmentName,
                        "mark":{
                            "c1":"NA",
                            "c2":"NA",
                            "c3":"NA",
                            "c4":"NA",
                            "c5":"NA",
                        }
                    })
                    continue
                marks.append({
                    "name":j.assessmentName,
                    "mark":marks_instance.marks
                })
            response_json["subjects"].append({
                "name":i.name,
                "marks":marks
            })
        return Response(response_json,status=status.HTTP_200_OK)

class GetOstuFA(APIView):

    authentication_classes=[]
    permission_classes=[]

    def get(self,format=None):
        grade=self.request.GET.get("grade",None)
        try:
            grade_instance=Grades.objects.get(name=grade)
        except Grades.DoesNotExist:
            return Response({
                "message":"Grade does not exists"
            },status=status.HTTP_400_BAD_REQUEST)

        assessments=Assessment.objects.filter(grade=grade_instance,assessmentType="FA",assessmentFor="subject")
        subjects=Subject.objects.filter(grade=grade_instance)
        students=Student.objects.filter(grade=grade)
        response_json={}
        response_json["assessment_list"]=[ass.assessmentName for ass in assessments]
        response_json["subject_list"]=[sub.name for sub in subjects]
        response_json["assessments"]={}
        response_json["student_list"]=[stud.name for stud in students]
        
        for i in assessments:
            
            response_json["assessments"][i.assessmentName]=[]
                
            
            for j in subjects:
                subject_data={
                    "name":j.name,
                    "students":[]
                }
                for k in students:
                    try:
                        mark_entry_instance=MarkEntry.objects.get(student=k,grade=grade_instance,assessment=i,subject_code=j)
                        subject_data["students"].append({
                            "name":k.name,
                            "c1":mark_entry_instance.marks["c1"],
                            "c2":mark_entry_instance.marks["c2"]
                        })
                    except MarkEntry.DoesNotExist:
                        subject_data["students"].append({
                            "name":k.name,
                            "c1":"NA",
                            "c2":"NA"
                        })
                response_json["assessments"][i.assessmentName].append(subject_data)
            
        return Response(response_json,status=status.HTTP_200_OK)
            

class GetOstuSA(APIView):

    authentication_classes=[]
    permission_classes=[]

    def get(self,format=None):
        grade=self.request.GET.get("grade",None)
        try:
            grade_instance=Grades.objects.get(name=grade)
        except Grades.DoesNotExist:
            return Response({
                "message":"Grade does not exists"
            },status=status.HTTP_400_BAD_REQUEST)

        assessments=Assessment.objects.filter(grade=grade_instance,assessmentType="SA",assessmentFor="subject")
        subjects=Subject.objects.filter(grade=grade_instance)
        students=Student.objects.filter(grade=grade)
        response_json={}
        response_json["assessment_list"]=[ass.assessmentName for ass in assessments]
        response_json["subject_list"]=[sub.name for sub in subjects]
        response_json["assessments"]={}
        response_json["student_list"]=[stud.name for stud in students]
        
        for i in assessments:
            
            response_json["assessments"][i.assessmentName]=[]
                
            
            for j in subjects:
                subject_data={
                    "name":j.name,
                    "students":[]
                }
                for k in students:
                    try:
                        mark_entry_instance=MarkEntry.objects.get(student=k,grade=grade_instance,assessment=i,subject_code=j)
                        subject_data["students"].append({
                            "name":k.name,
                            "c1":mark_entry_instance.marks["c1"],
                            "c2":mark_entry_instance.marks["c2"],
                            "c3":mark_entry_instance.marks["c3"],
                            "c4":mark_entry_instance.marks["c4"],
                            "c5":mark_entry_instance.marks["c5"],
                            
                        })
                    except MarkEntry.DoesNotExist:
                        subject_data["students"].append({
                            "name":k.name,
                            "c1":"NA",
                            "c2":"NA",
                            "c3":"NA",
                            "c4":"NA",
                            "c5":"NA"
                        })
                response_json["assessments"][i.assessmentName].append(subject_data)
            
        return Response(response_json,status=status.HTTP_200_OK)

class GetOUOI(APIView):

    authentication_classes=[]
    permission_classes=[]

    def get(self,format=None):
        grade=self.request.GET.get("grade",None)
        try:
            grade_instance=Grades.objects.get(name=grade)
        except Grades.DoesNotExist:
            return Response({
                "message":"Grade does not exists"
            },status=status.HTTP_400_BAD_REQUEST)

        assessments=Assessment.objects.filter(grade=grade_instance,assessmentType="FA",assessmentFor="UOI")
        themes=Theme.objects.filter(grade=grade_instance)
        students=Student.objects.filter(grade=grade)
        response_json={}
        response_json["assessment_list"]=[ass.assessmentName for ass in assessments]
        response_json["theme_list"]=[sub.name for sub in themes]
        response_json["assessments"]=[]
        response_json["student_list"]=[stud.name for stud in students]

        """
        response_json["assessments"].append({
                "name":i.name,
                "marks":[
                    {
                        "name":"FA1",
                        "students":[
                            {
                                "name":"Aravind",
                                "c1":0,
                                "c2":6
                            }
                        ]
                    }
                ]
            })
            
        """
        for i in themes:
            theme_object={
                "name":i.name,
                "marks":[]
            }
            assessments=Assessment.objects.filter(grade=grade_instance,assessmentType="FA",assessmentFor="UOI",theme=i)

            for j in assessments:
                ass_object={
                    "name":j.assessmentName,
                    "students":[]
                }
                for k in students:
                    try:
                        mark_entry_instance=MarkEntry.objects.get(student=k,grade=grade_instance,assessment=j,theme=i)
                        ass_object["students"].append({
                            "name":k.name,
                            "c1":mark_entry_instance.marks["c1"],
                            "c2":mark_entry_instance.marks["c2"]
                        })
                    except MarkEntry.DoesNotExist:
                        ass_object["students"].append({
                            "name":k.name,
                            "c1":"NA",
                            "c2":"NA"
                        })
                theme_object["marks"].append(ass_object)
            response_json["assessments"].append(theme_object)
        return Response(response_json,status=status.HTTP_200_OK)

class GetUOISa(APIView):

    authentication_classes=[]
    permission_classes=[]

    def get(self,format=None):
        grade=self.request.GET.get("grade",None)
        try:
            grade_instance=Grades.objects.get(name=grade)
        except Grades.DoesNotExist:
            return Response({
                "message":"Grade does not exists"
            },status=status.HTTP_400_BAD_REQUEST)

        assessments=Assessment.objects.filter(grade=grade_instance,assessmentType="SA",assessmentFor="UOI")
        themes=Theme.objects.filter(grade=grade_instance)
        students=Student.objects.filter(grade=grade)
        response_json={}
        response_json["assessment_list"]=[ass.assessmentName for ass in assessments]
        response_json["theme_list"]=[sub.name for sub in themes]
        response_json["assessments"]=[]
        response_json["student_list"]=[stud.name for stud in students]

        """
        response_json["assessments"].append({
                "name":i.name,
                "marks":[
                    {
                        "name":"FA1",
                        "students":[
                            {
                                "name":"Aravind",
                                "c1":0,
                                "c2":6
                            }
                        ]
                    }
                ]
            })
            
        """
        for i in themes:
            theme_object={
                "name":i.name,
                "marks":[]
            }
            assessments=Assessment.objects.filter(grade=grade_instance,assessmentType="SA",assessmentFor="UOI",theme=i)

            for j in assessments:
                ass_object={
                    "name":j.assessmentName,
                    "students":[]
                }
                for k in students:
                    try:
                        mark_entry_instance=MarkEntry.objects.get(student=k,grade=grade_instance,assessment=j,theme=i)
                        ass_object["students"].append({
                            "name":k.name,
                            "c1":mark_entry_instance.marks["c1"],
                            "c2":mark_entry_instance.marks["c2"],
                            "c3":mark_entry_instance.marks["c3"],
                            "c4":mark_entry_instance.marks["c4"],
                            "c5":mark_entry_instance.marks["c5"]
                            
                        })
                    except MarkEntry.DoesNotExist:
                        ass_object["students"].append({
                            "name":k.name,
                            "c1":"NA",
                            "c2":"NA",
                            "c3":"NA",
                            "c4":"NA",
                            "c5":"NA"
                        })
                theme_object["marks"].append(ass_object)
            response_json["assessments"].append(theme_object)
        return Response(response_json,status=status.HTTP_200_OK)