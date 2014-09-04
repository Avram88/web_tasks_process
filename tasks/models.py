from django.db import models
from django.contrib.auth.models import User, Group

class BaseModel(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
        
    class Meta:
        abstract = True
    
class WorkflowInst(BaseModel):
    type = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    class Meta:
        db_table = 'workflow_inst'

class TaskInst(BaseModel):    
    name = models.CharField(max_length=200)
    ordinal = models.PositiveIntegerField()
    deadline = models.DateTimeField()
    description = models.TextField()
    finished = models.BooleanField(default = False)    
    
    workflow = models.ForeignKey(WorkflowInst)
    user = models.ForeignKey(User, null=True)
    role = models.ForeignKey(Group)
    class Meta:
        db_table = 'task_inst'