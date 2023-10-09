from django.db import models

# Create your models here.
class Grades(models.Model):

    name=models.CharField(max_length=25)
    section=models.JSONField()

    def __str__(self):
        return str(self.id)+self.name


class Student(models.Model):

    name=models.CharField(max_length=256)
    grade=models.CharField(max_length=25)
    section=models.CharField(max_length=23)
    usn=models.CharField(max_length=25,unique=True)

    def __str__(self):
        return str(self.id)+self.usn

class Subject(models.Model):

    grade=models.ForeignKey(Grades,on_delete=models.CASCADE)
    name=models.CharField(max_length=25)
    subject_code=models.CharField(max_length=30)

    def __str__(self):
        return self.name+str(self.id)
    
class Theme(models.Model):

    grade=models.ForeignKey(Grades,on_delete=models.CASCADE)
    name=models.CharField(max_length=25)
    centralidea=models.CharField(max_length=25)
    lineofinquiry=models.CharField(max_length=25)

    def __str__(self):
        return self.name+str(self.id)

class Assessment(models.Model):
    assessmentType=models.CharField(max_length=256)
    assessmentName=models.CharField(max_length=256)
    assessmentFor=models.CharField(max_length=10)
    theme=models.ForeignKey(Theme,on_delete=models.CASCADE,null=True,blank=True)
    subject=models.ManyToManyField(Subject,null=True,blank=True)
    grade=models.ForeignKey(Grades,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+self.assessmentName

class MarkEntry(models.Model):

    assessment=models.ForeignKey(Assessment,on_delete=models.CASCADE)
    grade=models.ForeignKey(Grades,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    theme=models.ForeignKey(Theme,on_delete=models.CASCADE,null=True,blank=True)
    marks=models.JSONField(null=True,blank=True)

    def __str__(self):
        return str(self.id)
