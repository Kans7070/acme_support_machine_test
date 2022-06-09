from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from apps.custom_admin.forms import CreateDepartmentForm, CreateUserForm
from apps.user.models import User
from apps.custom_admin.models import Department


# Create your views here.


@login_required(redirect_field_name=None, login_url='admin_login')
def home(request):
    users = User.objects.all().exclude(role='Admin')
    context = {
        'users': users
    }
    return render(request, 'admin/home_page.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('admin_home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        admin = auth.authenticate(email=email, password=password)
        if admin:
            if admin.role == 'Admin':
                auth.login(request, admin)
                return redirect('admin_home')
        messages.error(request, 'invalid credentials')

    return render(request, 'accounts/login.html')


@login_required(redirect_field_name=None, login_url='admin_login')
def logout(request):
    auth.logout(request)
    return redirect('admin_login')


@login_required(redirect_field_name=None, login_url='admin_login')
def create_user(request):
    form = CreateUserForm()
    if request.method == 'POST':
        admin=request.user.email
        print(admin)
        if User.objects.filter(email=request.POST['email']).exists():
            messages.error(request, 'Email already exists')
        elif User.objects.filter(phone_number=request.POST['phone_number']).exists():
            messages.error(request, 'Phone number already exists')
        else:    
            department=Department.object.get(id=request.POST['department'])
            user = User.objects.create_user(
                name=request.POST['name'], 
                email=request.POST['email'], 
                phone_number=request.POST['phone_number'],
                password=request.POST['password'], 
                department=department, 
                created_by=admin
                )

            if user:
                return redirect('admin_home')
    context = {
        'form': form,
    }
    return render(request, 'admin/create_user_page.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def department(request):
    departments=Department.object.all()
    context={
        'departments': departments
    }
    return render(request, 'admin/department_page.html',context)


@login_required(redirect_field_name=None, login_url='admin_login')
def create_department(request):
    form = CreateDepartmentForm()
    if request.method == 'POST':
        if Department.object.filter(name=request.POST['name']).exists():
            messages.error(request, 'this department already exists')
        else:    
            admin=request.user.email 
            name=request.POST['name']
            department = Department.object.create_department(
                name=name.upper(), 
                description=request.POST['description'],
                created_by=admin
                )
            if department:
                return redirect('department_page')
    context = {
        'form': form,
        'url_name':'admin_create_department',
    }
    return render(request, 'admin/create_department_page.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def edit_department(request,pk):
    department = Department.object.get(id=pk)
    form = CreateDepartmentForm(instance=department)
    if request.method == 'POST':
        data = {}
        for x in request.POST:
            data[x] = request.POST[x]
        data['name'] = data['name'].upper()
        if Department.object.filter(name=request.POST['name']).exclude(id=pk).exists():
            messages.error(request, 'this department already exists')
        else:    
            form = CreateDepartmentForm(data, instance=department)  
            if form.is_valid():
                form.save()
                return redirect('department_page')
            else: 
                messages.error(request, 'invalid form')            
    context = {
        'form': form,
    }
    return render(request, 'admin/create_department_page.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def delete_department(request,pk):
    department = Department.object.get(id=pk)
    user = User.objects.filter(department=department)
    if user:
        messages.error(request,'Department has an active user')
    else:
        department.delete()
        messages.success(request,'Department has deleted')
    return redirect('department_page')

