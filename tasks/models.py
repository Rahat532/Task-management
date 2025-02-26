from django.db import models
from django.db.models.signals import post_save,pre_save,m2m_changed,post_delete,pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail


# class Employee
class Employee(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

# Create your models here.
class Project(models.Model):
    name =models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    start_date=models.DateTimeField()
    def __str__(self):
        return self.name


class Tasks(models.Model):
    STATUS_CHOICES = [
        ('PENDING','Pending'),
        ('IN_PROGRESS','In progress'),
        ('COMPLETED','Completed'),
        
    ]
    assigned_to=models.ManyToManyField(Employee,related_name='tasks')
    project =models.ForeignKey(Project,on_delete=models.CASCADE,default=1,related_name='project_name')
    title=models.CharField(max_length=250)
    description=models.TextField()
    due_date=models.DateField()
    status=models.CharField(
        max_length=20,choices=STATUS_CHOICES,default="PENDING"
    )
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


class TaskDetail(models.Model):
    HIGH = "H"
    MEDIUM = "M"
    LOW = "L"
    PRIORITY_OPTIONS=(
        ('LOW','Low'),
        ('MEDIUM','Medium'),
        ('HIGH','High'),
    )
    task=models.OneToOneField(Tasks,
                              on_delete=models.DO_NOTHING,
                              related_name="details")
    # assigned_to=models.CharField(max_length=100)
    priority=models.CharField(max_length=6, choices=PRIORITY_OPTIONS,default='LOW')
    notes=models.TextField(blank=True,null=True)
    def __str__(self):
        return f"Details for Task{self.task.title}"
    
   #  Signals 

@receiver(m2m_changed,sender=Tasks.assigned_to.through)
def notify_employees_on_task_created(sender,instance,action,**kwargs):
    if action=='post_add':
       assigned_email=[emp.email for emp in instance.assigned_to.all()]
       
       send_mail(
            "New Tasks Assigned",
            f"You have been assigned to  the task :{instance.title}",
            "abdullahalrahat4261@gmail.com",
            assigned_email,
            fail_silently=False,
            
        )
@receiver(post_delete,sender=Tasks)
def delete_associate_details(sender,instance,**kwargs):
    if instance.details:
        print(isinstance)
        instance.details.delete()
        
        print("The Task has been deleted successfully")