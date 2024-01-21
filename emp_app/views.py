from django.shortcuts import render, HttpResponse, redirect
from . models import Role, department, employee
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, 'index.html')


def all_emp(request):
    emps=employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render (request, 'all_emp.html', context)



def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        new_emp = employee(first_name= first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept_id = dept, role_id = role, hire_date = datetime.now())
        new_emp.save()
        return HttpResponse('Employee added Successfully')
    elif request.method=='GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("An Exception Occured! Employee Has Not Been Added")


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("employee deleted")
        except:
            return HttpResponse("please enter a valid employee id")
    emps=employee.objects.all()
    context = {
        'emps': emps
    }

    return render (request, 'remove_emp.html', context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains = role)

        context = {
            'emps': emps
        }
        return render(request, 'all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An Exception Occurred')
    
def update_emp(request):
    pass

def signup(request):
    if request.method=="POST":
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("password not match with confirm password")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    
    return render(request,"signup.html")



def login(request):
    if request.method=="POST":
        uname=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request, username=uname, password=pass1)
        if user is not None:
            return redirect('index')
        else:
            return HttpResponse("user name or password id incorrect")

    return render(request, "login.html")

def logout(request):
    return redirect('login')