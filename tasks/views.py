from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import glob, os

@login_required
def index(request):        
    model_dir = "D:\\Fax\\master_rad\\projekat\\web_tasks_process\\tasks\\models\\"
    ext =  "*.wf"
    models = glob.glob(model_dir + ext)
    
    model_names = []
    
    for file_name in models:
        model_names.append(os.path.basename(file_name)[:-3])   
                
    return render(request, 'tasks/index.html', {'model_names':model_names})
    
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
    