from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from apps.custom_admin.forms import CreateDepartmentForm, CreateUserForm
from apps.user.models import User
from apps.custom_admin.models import Department


# Create your views here.


def is_admin(request):
    if request.user.role == 'Admin':
        return True
    return False


@login_required(redirect_field_name=None, login_url='admin_login')
def home(request):
    if not is_admin(request):
        print(is_admin(request))
        return redirect('user_home')
    users = User.objects.all().exclude(role='Admin')
    context = {
        'users': users,
        'is_admin': 'True',
        'title': 'Admin User Page'
    }
    return render(request, 'user_manage_page.html', context)


def login(request):
    if request.user.is_authenticated and not is_admin(request):
        return redirect('user_home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        admin = auth.authenticate(email=email, password=password)
        if admin:
            if admin.role == 'Admin':
                auth.login(request, admin)
                return redirect('admin_home')
        messages.error(request, 'invalid credentials')
    context = {
        'field': 'Email',
        'is_admin': 'True',
        'title': 'Admin Login'
    }
    return render(request, 'accounts/login.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def create_user(request):
    if not is_admin(request):
        return redirect('user_home')
    form = CreateUserForm()
    if request.method == 'POST':
        admin = str(request.user.email)
        print(admin)
        if User.objects.filter(email=request.POST['email']).exists():
            messages.error(request, 'Email already exists')
        elif User.objects.filter(phone_number=request.POST['phone_number']).exists():
            messages.error(request, 'Phone number already exists')
        else:
            department = Department.object.get(id=request.POST['department'])
            user = User.objects.create_user(
                name=request.POST['name'],
                email=request.POST['email'],
                phone_number=request.POST['phone_number'],
                password=request.POST['password'],
                department=department,
                created_by=admin,
            )
            if user:
                return redirect('admin_home')
    context = {
        'form': form,
        'title': 'Create User',
        'is_admin': 'True'
    }
    return render(request, 'form_page.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def department(request):
    if not is_admin(request):
        return redirect('user_home')
    departments = Department.object.all()
    context = {
        'departments': departments,
        'is_admin': 'True'
    }
    return render(request, 'department_manage_page.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def create_department(request):
    if not is_admin(request):
        return redirect('user_home')
    form = CreateDepartmentForm()
    if request.method == 'POST':
        if Department.object.filter(name=request.POST['name']).exists():
            messages.error(request, 'this department already exists')
        else:
            admin = request.user.email
            name = request.POST['name']
            department = Department.object.create_department(
                name=name.upper(),
                description=request.POST['description'],
                created_by=admin
            )
            if department:
                return redirect('department_page')
    context = {
        'form': form,
        'title': 'Create Department',
        'is_admin': 'True'
    }
    return render(request, 'form_page.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def edit_department(request, pk):
    if not is_admin(request):
        return redirect('user_home')
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
        'title': 'Edit Department',
        'is_admin': 'True'
    }
    return render(request, 'form_page.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def delete_department(request, pk):
    if not is_admin(request):
        return redirect('user_home')
    department = Department.object.get(id=pk)
    user = User.objects.filter(department=department)
    if user:
        messages.error(request, 'Selected department has an active user')
    else:
        department.delete()
        messages.success(request, 'Department has deleted')
    return redirect('department_page')



def logout(request):
    if request.user.is_authenticated:
        if is_admin(request):
            auth.logout(request)
            return redirect('admin_login')
        else:
            auth.logout(request)
            return redirect('user_login')