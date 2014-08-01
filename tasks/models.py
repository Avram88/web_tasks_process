from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    user = models.ForeignKey(User)
    
    class Meta:
        abstract = True
    
class WorkflowInst(BaseModel):
    type = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'workflow_inst'

class TaskInst(BaseModel):    
    name = models.CharField(max_length=200)
    ordinal = models.PositiveIntegerField()
    deadline = models.DateTimeField()
    description = models.TextField()
    finished = models.BooleanField(default = False)    
    
    workflow = models.ForeignKey(WorkflowInst)
        
    class Meta:
        db_table = 'task_inst'