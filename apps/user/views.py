from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from apps.user.backend import AuthBackend
from apps.zdesk import ticket_show


# Create your views here.

@login_required(redirect_field_name=None, login_url='user_login')
def home(request):
    datas=ticket_show()
    context = {
        'title': 'Tickets'

    }
    return render(request, 'ticket_manage_page.html',context)


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


