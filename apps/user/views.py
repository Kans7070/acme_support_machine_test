from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import auth,messages

# Create your views here.

def home(request):
    return HttpResponse('haii')

def login(request):
    if request.user.is_authenticated:
        return redirect('user_home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            return redirect('user_home')
        messages.error(request, 'invalid credentials')
    context = {
        'module': 'User',
        'field':'Email or Phone No',
    }
    return render(request, 'accounts/login.html',context)
