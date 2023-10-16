from django.urls import path
from .views import *
urlpatterns = [
    path("get-grades/",GetGrades.as_view()),
    path("new-grade/",CreateGrades.as_view()),
    path("create-student/",CreateStudent.as_view()),
    path("create-subject/",CreateSubject.as_view()),
    path("create-theme/",CreateTheme.as_view()),
    path("create-assessment/",CreateAssessment.as_view()),
    path("get-students/",GetStudentList.as_view()),
    path("update-marks/",UpdateMarks.as_view()),
    path("get-grade/",GetGradeDetails.as_view()),
    path("get-themes/",GetThemes.as_view()),
    path("get-subjects/",GetSubjects.as_view()),
]
