from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import Sum
from .models import *
from django.db.models import Q
# Create your views here.


def home(request):
    return render(request, "index.html")


def contact(request):
    return render(request, 'contact.html')


def login(request):
    if request.POST:
        uname = request.POST["name"]
        pwd = request.POST["pass"]
        user = authenticate(username=uname, password=pwd)
        if user is None:
            messages.info(request, 'Username or password is incorrect')
        else:
            userdata = User.objects.get(username=uname)
            if userdata.is_superuser == 1:
                return redirect("/adminhome")
            elif userdata.is_staff == 1:
                request.session["email"] = uname
                r = Teachers.objects.get(email=uname)
                request.session["id"] = r.id
                request.session["name"] = r.name
                return redirect("/hodhome")
            else:
                request.session["email"] = uname
                r = Student.objects.get(email=uname)
                request.session["id"] = r.id
                request.session["name"] = r.name
                return redirect("/studenthome")

    return render(request, "login.html")


def adminhome(request):
    return render(request, "adminhome.html")


def hodhome(request):
    return render(request, "hodhome.html")


def studenthome(request):
    return render(request, "studenthome.html")


def studentsoft(request):
    id = request.session['id']
    stu = Student.objects.get(id=id)
    if request.POST:
        search = request.POST['search']
        data = Software.objects.filter(Q(course__course__contains=search) | Q(
            title__contains=search) | Q(desc__contains=search))
    else:
        data = Software.objects.filter(course__id=stu.course.id)
    return render(request, "studentsoft.html", {"data": data})


def teachersoft(request):
    id = request.session['id']
    stu = Teachers.objects.get(id=id)
    if request.POST:
        search = request.POST['search']
        data = Software.objects.filter(Q(course__course__contains=search) | Q(
            title__contains=search) | Q(desc__contains=search))
    else:
        data = Software.objects.filter(
            course__department__id=stu.department.id)
    return render(request, "teachersoft.html", {"data": data})

######################################################################
#                           ADMIN PAGES

######################################################################


def addhod(request):
    if request.POST:
        name = request.POST["name"]
        department = request.POST['department']
        email = request.POST["email"]
        contact = request.POST["contact"]
        password = request.POST['password']

        User_exist = User.objects.filter(username=email).exists()
        if not User_exist:
            try:
                dept = Department.objects.get(id=department)
                u = User.objects.create_user(
                    username=email, password=password, is_superuser=0, is_active=1, is_staff=1)
                u.save()
                r = Teachers.objects.create(
                    name=name, department=dept, email=email, contact=contact, user=u)
                r.save()
            except Exception as e:
                messages.info(request, e)
            else:
                messages.info(request, 'Registration successful')
        else:
            messages.info(request, 'Email already registered')
    depts = Department.objects.all()
    return render(request, "addhod.html", {"depts": depts})


def addstudent(request):
    if request.POST:
        regno = request.POST["regno"]
        name = request.POST["name"]
        semester = request.POST["semester"]
        year = request.POST["year"]
        contact = request.POST["contact"]
        email = request.POST["email"]
        course = request.POST["course"]
        password = request.POST["pass"]
        if Student.objects.filter(regno=regno).exists():
            messages.info(request, 'Register Number already Exists')
        else:
            if User.objects.filter(username=email).exists():
                messages.info(request, 'Email already exists')
            else:
                c = Course.objects.get(id=course)
                u = User.objects.create_user(
                    username=email, password=password, is_superuser=0, is_active=1, is_staff=0)
                u.save()
                r = Student.objects.create(
                    regno=regno, name=name, semester=semester, year=year, contact=contact, email=email, course=c, user=u)
                r.save()
                messages.info(request, 'Registration successful')
    cou = Course.objects.all()
    return render(request, "addstudent.html", {"course": cou})


def adminteachers(request):

    data = Teachers.objects.all().order_by("-id")
    return render(request, "adminteachers.html", {"data": data})


def adminstudents(request):

    data = Student.objects.all().order_by("-id")
    return render(request, "adminstudents.html", {"data": data})


def admindeleteteacher(request):
    id = request.GET['id']
    usr = User.objects.get(id=id)
    usr.delete()
    return redirect("/adminteachers")


def admindeletestudents(request):
    id = request.GET['id']
    usr = User.objects.get(id=id)
    usr.delete()
    return redirect("/adminstudents")


def hoddeletestudent(request):
    id = request.GET.get("id")
    email = request.GET.get("email")
    Student.objects.filter(id=id).delete()
    User.objects.filter(username=email).delete()
    return redirect("/addstudent")

def adminsoftware(request):
    if request.POST:
        title = request.POST["title"]
        desc = request.POST["desc"]
        soft = request.FILES["soft"]
        course = request.POST["course"]
        if Software.objects.filter(title=title, course=course).exists():
            messages.info(request, 'Subject already exists')
        else:
            c = Course.objects.get(id=course)
            sub = Software.objects.create(
                title=title, desc=desc, file=soft, course=c)
            sub.save()
            messages.info(request, 'Subject added')
    data = Software.objects.all()
    course = Course.objects.all()
    return render(request, "adminsoftware.html", {"data": data, "course": course})


def admindeletesoft(request):
    id = request.GET.get("id")
    Software.objects.filter(id=id).delete()
    return redirect("/adminsoftware")


def adddepartments(request):
    data = Department.objects.all()
    if request.POST:
        dept = request.POST['dept']
        de = Department.objects.create(department=dept)
        de.save()
    return render(request, "adddepartments.html", {"data": data})


def editdepartment(request):
    id = request.GET['id']
    data = Department.objects.all()
    cData = Department.objects.get(id=id)
    if request.POST:
        dept = request.POST['dept']
        cData.department = dept
        cData.save()
        return redirect("/adddepartments")
    return render(request, "editdepartment.html", {"data": data, "cData": cData})


def deletedepartment(request):
    id = request.GET['id']
    cData = Department.objects.get(id=id)
    cData.delete()
    return redirect("/adddepartments")


def addcourse(request):
    data = Course.objects.all()
    dept = Department.objects.all()
    if request.POST:
        dept = request.POST['dept']
        course = request.POST['course']
        d = Department.objects.get(id=dept)
        de = Course.objects.create(department=d, course=course)
        de.save()
        return redirect("/addcourse")
    return render(request, "addcourse.html", {"data": data, "dept": dept})


def editcourse(request):
    id = request.GET['id']
    data = Course.objects.all()
    dept = Department.objects.all()
    cCourse = Course.objects.get(id=id)
    if request.POST:
        dept = request.POST['dept']
        course = request.POST['course']
        cCourse.course = course
        cCourse.save()
        return redirect("/addcourse")
    return render(request, "editcourse.html", {"data": data, "dept": dept, "cCourse": cCourse})


def deletecourse(request):
    id = request.GET['id']
    cCourse = Course.objects.get(id=id)
    cCourse.delete()
    return redirect("/addcourse")
