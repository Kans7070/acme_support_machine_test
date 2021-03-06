from time import time
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from apps.custom_admin.forms import CreateDepartmentForm, CreateUserForm, TicketForm
from apps.user.models import User
from apps.custom_admin.models import Department
from datetime import date, datetime

from apps.zdesk import create_ticket, ticket_show, create_user as zendesk_create_user,delete_ticket as zendesk_delete_ticket


# Create your views here.


def is_admin(request):
    if request.user.role == 'Admin':
        return True
    return False

def data_colector(request):
    
    try:
        data={
            'subject':'',
            'description':'',
            'priority':'',
            'custom_fields':[
                {
                    'id':'5482342024221',
                    'value':''
                    },
                {
                    'id':'5482248733085',
                    'value':''
                    }

            ]
        }
        data['subject']=request.POST['subject']
        data['description'] = request.POST['description']
        data['priority'] = request.POST['priority']
        data['custom_fields'][0]['value'] = request.user.email
        data['custom_fields'][1]['value'] = request.user.phone_number
    except:
        data['email'] = request.POST['email']
        data['phone'] = request.POST['phone_number']
        data['name'] = request.POST['name']
        
    return data


@login_required(redirect_field_name=None, login_url='admin_login')
def home(request):
    if not is_admin(request):
        return redirect('user_home')
    users = User.objects.all().exclude(role='Admin')
    context = {
        'users': users,
        'is_admin': True,
        'title': 'Users'
    }
    return render(request, 'user_manage_page.html', context)


def login(request):
    if request.user.is_authenticated:
        if  not is_admin(request):
            return redirect('user_home')
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
    context = {
        'field': 'Email',
        'is_admin': True,
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
        if User.objects.filter(email=request.POST['email']).exists():
            messages.error(request, 'Email already exists')
        elif User.objects.filter(phone_number=request.POST['phone_number']).exists():
            messages.error(request, 'Phone number already exists')
        else:
            department = Department.object.get(id=request.POST['department'])
            data = zendesk_create_user(data_colector(request))
            user = User.objects.create_user(
                name=request.POST['name'],
                email=request.POST['email'],
                phone_number=request.POST['phone_number'],
                password=request.POST['password'],
                department=department,
                created_by=admin,
            )
            user.id = data
            user.save()
            messages.success(request, 'User created successfully')
            if user:

                return redirect('admin_home')
    context = {
        'form': form,
        'title': 'Create User',
        'is_admin': True
    }
    return render(request, 'form_page.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def department(request):
    if not is_admin(request):
        return redirect('user_home')
    departments = Department.object.all()
    context = {
        'departments': departments,
        'title': 'Departments',
        'is_admin': True
    }
    return render(request, 'department_manage_page.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def create_department(request):
    if not is_admin(request):
        return redirect('user_home')
    form = CreateDepartmentForm()
    if request.method == 'POST':
        form = CreateDepartmentForm(request.POST)
        if Department.object.filter(name=request.POST['name']).exists():

            messages.error(request, 'this department already exists')
        else:
            if form.is_valid():
                form.instance.created_by = request.user.email
                form.save()
                return redirect('department_page')
            else:
                messages.error(request, form.errors)
    context = {
        'form': form,
        'title': 'Create Department',
        'is_admin': True
    }
    return render(request, 'form_page.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def edit_department(request, pk):
    if not is_admin(request):
        return redirect('user_home')
    department = Department.object.get(id=pk)
    form = CreateDepartmentForm(instance=department)
    if request.method == 'POST':
        form = CreateDepartmentForm(request.POST, instance=department)
        if Department.object.filter(name=request.POST['name'].upper()).exists():
            messages.error(request, 'this department already exists')
        else:
            if form.is_valid():
                form.save()

                return redirect('department_page')
            else:
                messages.error(request, form.errors)
    context = {
        'form': form,
        'title': 'Edit Department',
        'is_admin': True
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


@login_required(redirect_field_name=None, login_url='admin_login')
def admin_ticket(request):
    if not is_admin(request):
        return redirect('user_home')
    datas=ticket_show()
    try:
        datas = datas['tickets']
    except:
        datas=''
    context = {
        'title': 'Tickets',
        'is_admin': True,
        'datas':datas
    }
    return render(request, 'ticket_manage_page.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def admin_create_ticket(request):
    if not is_admin(request):
        return redirect('user_home')
    form = TicketForm()
    if request.method == 'POST':
        data = data_colector(request)
        form = TicketForm(data)
        if form.is_valid():
            form.save(data)
            messages.success(request,'Ticket has been created successfully')
            return redirect('admin_ticket_page')
    context = {
        'title': 'Create Tickets',
        'form': form,
    }
    return render(request, 'form_page.html',context)


@login_required(redirect_field_name=None, login_url='admin_login')
def delete_ticket(request,pk):
    pk=str(pk)
    zendesk_delete_ticket(pk)
    messages.success(request, 'Deleted the ticket'+pk)
    return redirect('admin_ticket_page')


def logout(request):
    if request.user.is_authenticated:
        if is_admin(request):
            auth.logout(request)
            return redirect('admin_login')
        else:
            auth.logout(request)
            return redirect('user_login')
