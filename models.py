from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Department(models.Model):
    department = models.CharField(max_length=30)


class Teachers(models.Model):
    name = models.CharField(max_length=30)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=50)
    contact = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Course(models.Model):
    course = models.CharField(max_length=30, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True)


class Student(models.Model):
    regno = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=30)
    semester = models.CharField(max_length=50, null=True)
    year = models.CharField(max_length=25, null=True)
    email = models.EmailField(max_length=50)
    contact = models.BigIntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Software(models.Model):
    date = models.DateField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=25, null=True)
    desc = models.CharField(max_length=250, null=True)
    file = models.FileField(upload_to="File")
