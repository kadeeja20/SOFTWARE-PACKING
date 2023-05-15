"""examhall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from spApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('login', views.login),
    path('adminhome', views.adminhome),
    path('addhod', views.addhod),
    path('hodhome', views.hodhome),
    path('addstudent', views.addstudent),
    path('studenthome', views.studenthome),
    path('studentsoft', views.studentsoft),
    path('teachersoft', views.teachersoft),
    path('adminsoftware', views.adminsoftware),
    path('adminteachers', views.adminteachers),
    path('adminstudents', views.adminstudents),
    path('admindeleteteacher', views.admindeleteteacher),
    path('admindeletestudents', views.admindeletestudents),
    path('adddepartments', views.adddepartments),
    path('editdepartment', views.editdepartment),
    path('deletedepartment', views.deletedepartment),
    path('addcourse', views.addcourse),
    path('editcourse', views.editcourse),
    path('deletecourse', views.deletecourse),
    path('admindeletesoft', views.admindeletesoft),
    path('contact', views.contact),







]
