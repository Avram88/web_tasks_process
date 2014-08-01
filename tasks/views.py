from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def index(request):    
    return render(request, 'tasks/index.html')
    
def auth_login(request):    
    return render(request, 'tasks/login.html')
    
def auth_logout(request):
    logout(request)
    return render(request, 'tasks/login.html')
    
def sign_in(request):       
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render(request, 'tasks/index.html',{'user':user})
        else:
            return render(request, 'tasks/login.html')
    else:
        return render(request, 'tasks/login.html')
    