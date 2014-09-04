from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import glob, os
from semantics import get_workflow_object
from models import TaskInst, WorkflowInst

@login_required
def index(request):        
    model_dir = "D:\\Fax\\master_rad\\projekat\\web_tasks_process\\tasks\\models\\"
    ext = "*.wf"
    models = glob.glob(model_dir + ext)
    
    model_names = []
    
    for file_name in models:
        model_names.append(os.path.basename(file_name)[:-3])   
                    
    user_roles = request.user.groups.all()
                    
    tasks = TaskInst.objects.filter(finished = False, role = user_roles[0])
                
    return render(request, 'tasks/index.html', {'model_names':model_names, 'tasks':tasks})

def detail(request, task_id):   
    task = TaskInst.objects.get(pk=task_id)      
    model_name = WorkflowInst.objects.get(pk=task.workflow_id).type
    workflow_obj = get_workflow_object(model_name) 
    next_tasks = workflow_obj.get_next_task_names(task.name)
    
    return render(request, 'tasks/detail.html', {'task':task, 'next_tasks':next_tasks})
    
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
            return redirect('tasks:index')
        else:
            return redirect('tasks:login')
    else:
        return redirect('tasks:login')
    
def start_process(request, model_name):
    workflow_obj = get_workflow_object(model_name)    
    workflow_obj.start(request.user)
    
    return redirect('tasks:index')

def finish_task(request, task_id):
    next_task_name = request.POST.get('next_task_name', None)  
      
    task = TaskInst.objects.get(pk=task_id)
    model_name = WorkflowInst.objects.get(pk=task.workflow_id).type
    workflow_obj = get_workflow_object(model_name) 
    workflow_obj.start_next_task(task_id, next_task_name, request.user)
    
    return redirect('tasks:index')

