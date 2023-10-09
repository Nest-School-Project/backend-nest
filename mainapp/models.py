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
