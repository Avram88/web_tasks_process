from arpeggio import ZeroOrMore, Kwd, Optional, RegExMatch as _, ParserPython, \
    SemanticAction, OneOrMore, EOF
from models import WorkflowInst, TaskInst
from django.contrib.auth.models import Group
from django.utils import timezone
import os
from web_tasks_process.settings import PROJECT_PATH

def workflow():         return Kwd('workflow'), name, open_bracket, ZeroOrMore(role), Optional(description), OneOrMore(task), close_bracket, EOF
def task():             return Kwd('task'), name, open_bracket, ZeroOrMore(role), ZeroOrMore(nextTask), ZeroOrMore(grType), ZeroOrMore(endTime), ZeroOrMore(exitCondition), Optional(description), close_bracket
def nextTask():         return Kwd('next'), colon, OneOrMore(name, Optional(comma)), semicomma
def grType():           return Kwd('type'), colon, [Kwd('automatic'), Kwd('manual')], semicomma
def endTime():          return Kwd('deadline'), colon, time, semicomma
def exitCondition():    return Kwd('exitCondition'), colon, name, semicomma
def role():             return Kwd('role'), colon, OneOrMore(name, Optional(comma)), semicomma
def description():      return Kwd('description'), colon, quote, text, quote, semicomma

def time():             return days, colon, hours, colon, minutes

def days():             return number, _(r"D")
def hours():            return number, _(r"H")
def minutes():          return number, _(r"M")

def name():             return _(r"\w+")
def number():           return _(r"\d+")
def text():             return _(r"[\w\s]+")
    
def open_bracket():     return _(r"\(")
def close_bracket():    return _(r"\)")
def colon():            return _(r"\:")
def comma():            return _(r"\,")
def semicomma():        return _(r"\;")
def quote():            return _(r"\"") 

def get_workflow_object(model_name):
    model_dir = os.path.join(PROJECT_PATH, 'tasks\\models\\');
    full_path = model_dir + str(model_name) + ".wf"
    
    if os.path.exists(os.path.dirname(full_path)):
        f = open(full_path, "r")              
        parser = ParserPython(workflow, debug=True)
        _parse_tree = parser.parse(f.read()  ) 
        return parser.getASG()
    else:
        return False

class WorkflowSA(SemanticAction):            
    def first_pass(self, parser, node, children):        
        workflow = WorkflowOM()
        
        for child in children:
            if isinstance(child, TaskOM):
                child.workflow = workflow
                workflow.tasks.append(child)
            if isinstance(child, NameOM):   
                workflow.name = child.value      
            if isinstance(child, RoleOM):
                workflow.role = child
                
        return workflow
        
class TaskSA(SemanticAction):    
    def first_pass(self, parser, node, children):
        task = TaskOM()
        
        for child in children:
            if isinstance(child, NameOM):
                task.name = child.value
            if isinstance(child, NextTaskOM):
                task.next_tasks = child.names
            if isinstance(child, RoleOM):
                task.role = child.name
            if isinstance(child, DescriptionOM):
                task.description = child.text
            if isinstance(child, EndTimeOM):
                task.deadline = child
                
        return task
    
    def second_pass(self, sa_name, task):        
        """Replacing next task name with next task object"""
        
        next_tasks_obj = []
        
        for next_task_name in task.next_tasks:
            for next_task_obj in task.workflow.tasks:
                if next_task_name == next_task_obj.name:
                    next_tasks_obj.append(next_task_obj)
                    
        task.next_tasks = next_tasks_obj
                            
        return task

class NextTaskSA(SemanticAction):
    def first_pass(self, parser, node, children):
        nextTask = NextTaskOM()
        
        for child in children:
            if isinstance(child, NameOM):
                nextTask.names.append(child.value)
                
        return nextTask

class RoleSA(SemanticAction):
    def first_pass(self, parser, node, children):   
        role = RoleOM()
        
        for child in children:
            if isinstance(child, NameOM):
                role.name = child.value
           
        return role 

class DescriprionSA(SemanticAction):
    def first_pass(self, parser, node, children):   
        description = DescriptionOM()
        
        for child in children:
            if isinstance(child, TextOM):
                description.text = child.value
           
        return description 
    
class EndTimeSA(SemanticAction):
    def first_pass(self, parser, node, children): 
        endTime = EndTimeOM()
        
        for child in children:
            if isinstance(child, DaysOM):
                endTime.days = child.value
            if isinstance(child, HoursSA):
                endTime.hours = child.value
            if isinstance(child, MinutesSA):
                endTime.minutes = child.value
                
        return endTime
    
class DaysSA(SemanticAction):
    def first_pass(self, parser, node, children):
        days = DaysOM()
        
        for child in children:
            if isinstance(child, NumberSA):
                days.value = child
        
        return days
    
class HoursSA(SemanticAction):
    def first_pass(self, parser, node, children):
        hours = HoursOM()
        
        for child in children:
            if isinstance(child, NumberSA):
                hours.value = child.value
        
        return hours
    
class MinutesSA(SemanticAction):
    def first_pass(self, parser, node, children):
        minutes = MinutesOM()
        
        for child in children:
            if isinstance(child, NumberSA):
                minutes.value = child.value
        
        return minutes
    
class NumberSA(SemanticAction):
    def first_pass(self, parser, node, children):
        return NumberOM(str(node))

class NameSA(SemanticAction):    
    def first_pass(self, parser, node, children):       
        return NameOM(str(node))

class TextSA(SemanticAction):
    def first_pass(self, parser, node, children):       
        return TextOM(str(node))
    
workflow.sem = WorkflowSA()
task.sem = TaskSA() 
nextTask.sem = NextTaskSA()
name.sem = NameSA()
role.sem = RoleSA()
description.sem = DescriprionSA()
text.sem = TextSA()
number.sem = NumberSA()
endTime.sem = EndTimeSA()
days.sem = DaysSA()
hours.sem = HoursSA()
minutes.sem = MinutesSA()

class WorkflowOM():
    def __init__(self, name="", tasks=[], role = None):
        self.name = name
        self.tasks = tasks
        self.role = role
    
    def start(self, start_user):
        """Create workflow and first task of current workflow"""

        workflow_inst = WorkflowInst(type=self.name, start_date=timezone.now(), end_date=timezone.now(), user=start_user)
        workflow_inst.save()
        
        first_task_obj = self.tasks[0]        
        
        print 'avram'
        print first_task_obj.deadline.days
        #find group by name, __iexact for case-insensitive match
        group = Group.objects.get(name__iexact = first_task_obj.role)
        
        first_task_isnt = TaskInst(name=first_task_obj.name, ordinal=1, start_date=timezone.now(), end_date=timezone.now(),
                                   deadline = timezone.now(), description = first_task_obj.description, workflow = workflow_inst, role = group)
        first_task_isnt.save()
    
    def get_task(self, name):
        pass
    
    def get_next_task_names(self, name):
        names = []
        
        for task in self.tasks:
            if task.name == name:
                for next_task in task.next_tasks:
                    names.append(next_task.name)
                return names
        
        return None
    
    def start_next_task(self, task_id, next_task_name, finished_by_user):
        task = TaskInst.objects.get(pk=task_id)
        task.finished = True
        task.user = finished_by_user
        task.save()      
            
        if next_task_name is not None:         
                    
            for tsk in self.tasks:
                if tsk.name == next_task_name:
                    next_task_obj = tsk 
                    
            workflow_inst = WorkflowInst.objects.get(pk=task.workflow_id)   
                                      
            #find group by name, __iexact for case-insensitive match
            group = Group.objects.get(name__iexact = next_task_obj.role)
        
            next_task_inst = TaskInst(name = next_task_name, ordinal = task.ordinal + 1, start_date=timezone.now(), end_date=timezone.now(),
                                       deadline = timezone.now(), description = "next_task_desc", workflow = workflow_inst, role = group)
            next_task_inst.save()
            
class TaskOM():
    def __init__(self, name="", next_tasks=[], role = None, description = ""):
        self.name = name
        self.next_tasks = next_tasks
        self.role = role
        self.description = description

class NextTaskOM():
    def __init__(self, names=[]):
        self.names = names

class RoleOM():
    def __init__(self, name=""):
        self.name = name

class EndTimeOM():
    def __init__(self, time=None):
        self.days = days
        self.hours = hours
        self.minutes = minutes

class DaysOM():    def __init__(self, value=None):
        self.value = value

class HoursOM():
    def __init__(self, value=None):
        self.value = value

class MinutesOM():
    def __init__(self, value=None):
        self.value = value
        
class DescriptionOM():
    def __init__(self, text=""):
        self.text = text

class TextOM():
    def __init__(self,  value=None):
        self.value = value

class NumberOM():
    def __init__(self,  value=None):
        self.value = value

class NameOM(): 
    def __init__(self, value=None):
        self.value = value
    

