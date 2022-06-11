from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from apps.custom_admin.forms import TicketForm
from apps.custom_admin.views import data_colector, is_admin
from apps.user.backend import AuthBackend
from apps.zdesk import ticket_show


# Create your views here.

@login_required(redirect_field_name=None, login_url='user_login')
def home(request):
    if is_admin(request):
            return redirect('admin_login')
    datas=ticket_show(request.user.email)
    context = {
        'title': 'Tickets',
        'datas':datas
    }
    return render(request, 'ticket_manage_page.html',context)


@login_required(redirect_field_name=None, login_url='user_login')
def user_create_ticket(request):
    if is_admin(request):
            return redirect('admin_login')
    form = TicketForm()
    if request.method == 'POST':
        data = data_colector(request)
        form = TicketForm(data)
        if form.is_valid():
            form.save(data)
            messages.success(request,'ticket has been created successfully')
            return redirect('user_home')
    context = {
        'title': 'Create Tickets',
        'form': form,
    }
    return render(request, 'form_page.html',context)



def login(request):
    if request.user.is_authenticated:
        return redirect('user_home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = AuthBackend.authenticate(email,password)
        if user:
            auth.login(request, user)
            return redirect('user_home')
        messages.error(request, 'invalid credentials')
    context = {
        'Title': 'User Login',
        'field': 'Email or Phone No',
    }
    return render(request, 'accounts/login.html', context)


