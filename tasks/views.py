from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TasksModelForm,TaskDetailModelFrom
from tasks.models import *
from datetime import date
from django.db.models import Q,Count,Max,Min,Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.contrib.auth import get_user_model


def get_user_with_groups(user_id):
    """Fetch the user and their groups in a single query."""
    return get_user_model().objects.prefetch_related('groups').get(id=user_id)

def is_manager(user):
    """Check if the user is a manager."""
    return user.groups.filter(name__iexact='Manager').exists()

def is_employee(user):
    """Check if the user is an employee."""
    return user.groups.filter(name__iexact='Employee').exists()
# Create your views here.
@user_passes_test(is_manager,login_url='no-permission')
def manager_dashboard(request):
    type =request.GET.get('type','all')
    
    # task=Tasks.objects.select_related('details').prefetch_related('assigned_to').all()
    #getting Tasks count
    # total_tasks=task.count()
    # # pending tasks count
    # pending_task =Tasks.objects.filter(status="PENDING").count()
    # # completed tasks count
    # completed_task =Tasks.objects.filter(status="COMPLETED").count()
    # In progress tasks count
    # in_progress_task =Tasks.objects.filter(status="IN_PROGRESS").count()
    # using the the Aggregate 
    base_query=Tasks.objects.select_related('details').prefetch_related('assigned_to')
    counts=Tasks.objects.aggregate(
        total_tasks=Count('id'),
        pending_task=Count('id',filter=Q(status="PENDING")),
        completed_task=Count('id',filter=Q(status="COMPLETED")),
        in_progress_task=Count('id',filter=Q(status="IN_PROGRESS"))
    ) 
   
    if type == 'completed':
        task=base_query.filter(status="COMPLETED")
    elif type == 'in_progress':
        task=base_query.filter(status="IN_PROGRESS")
    elif type == 'pending':
        task=base_query.filter(status="PENDING")
    elif type == 'all':
        task=base_query.all()
    
    context ={
        'task':task,
        'counts':counts,
        # 'total_tasks':total_tasks,
        # 'pending_task':pending_task,
        # 'completed_task':completed_task,
        # 'in_progress_task':in_progress_task,
    }
    return render(request, 'dashboard/manager-dashboard.html',context)
@user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request, 'dashboard/user-dashboard.html')
def test(request):
    context={
        'names':["rahat","admin","user","manager"],
        'age':25,
    }
    return render(request, 'test.html', context)
@login_required
@permission_required('tasks.add_task',login_url='no-permission')
def create_task(request):
    #employees= Employee.objects.all()
   task_form= TasksModelForm()# for Get Methods
   task_detail_from=TaskDetailModelFrom()
    
   if request.method =="POST":
        task_form= TasksModelForm(request.POST)# for Get Methods
        task_detail_from=TaskDetailModelFrom(request.POST)
        
        if task_form.is_valid() and task_detail_from.is_valid() :
            '''For Model From Data'''
            task=task_form.save()
            task_detail=task_detail_from.save(commit=False)
            task_detail.task=task
            task_detail.save()
            
            messages.success(request, "Task created successfully")
            return redirect('create-task')
              
        '''For Django From Data'''
    
   context={"task_form": task_form,"task_detail_from": task_detail_from,}
   return render(request, 'task_from.html',context)
@login_required
@permission_required('tasks.change_task',login_url='no-permission')
def update_task(request,id):
    
   task=Tasks.objects.get(id=id)
   task_form= TasksModelForm(instance=task)# for Get Methods
   if task.details:
        task_detail_from=TaskDetailModelFrom(instance=task.details)
    
   if request.method =="POST":
        task_form= TasksModelForm(request.POST,instance=task)# for Get Methods
        task_detail_from=TaskDetailModelFrom(request.POST,instance=task.details)
        
        if task_form.is_valid() and task_detail_from.is_valid() :
            '''For Model From Data'''
            task=task_form.save()
            task_detail=task_detail_from.save(commit=False)
            task_detail.task=task
            task_detail.save()
            
            messages.success(request, "Task updated successfully")
            return redirect('create-task')
              
        '''For Django From Data'''
    
   context={"task_form": task_form,"task_detail_from": task_detail_from,}
   return render(request, 'task_from.html',context)

@login_required
@permission_required('tasks.delete_task',login_url='no-permission')
def delete_task(request,id):
    if request.method == 'POST':
        task = Tasks.objects.get(id=id)
        task.delete()
        messages.success(request, "Task deleted successfully")
        return redirect('Manager-Dashboard')
    else:
        messages.error(request, "something went wrong")
        return redirect('Manager-Dashboard')

@login_required
@permission_required('tasks.view_task',login_url='no-permission')
def view_task(request):
    # retrieve all Data from Tasks Model
    tasks=Tasks.objects.all()
    # retrieve a specific Tasks
    task_3=Tasks.objects.get(id=1)
    task_4=Tasks.objects.filter(status="PENDING")
    # show the task which due date is today
    tasks_5=Tasks.objects.filter(due_date=date.today())
    '''show the task  priority who is not low priority Tasks'''
    tasks_6=TaskDetail.objects.exclude(priority="L")
    '''show the task about and oprations which is "," and'''
    # task_7=Tasks.objects.filter(title__icontains="c",status="PENDING")
    """now the or oprations"""
    task_7=Tasks.objects.filter(Q(status="IN_PROGRESS")|Q(status="PENDING"))
    # Select_related (Foreignkey,OneToOneField)
    rel_tasks=Tasks.objects.select_related('details').all()
    # Tasks=TaskDEtail.objects.select_related('task').all()
    # tasks = Task.objects.select_related('Project').all()
    """ prefectch_relates(reverse Foreignkey,ManyToMany)"""
    
    # Aggregated
    Task_count=Tasks.objects.aggregate(num_task=Count('id'))
    # how many tasks in on the project
    task_9=Project.objects.annotate(num_task=Count('project_name'))
    return render(request, 'show_task.html',{'tasks':tasks,"task_3":task_3, 'task_4':task_4,'tasks_5':tasks_5,'tasks_6':tasks_6,'task_7':task_7,'rel_tasks':rel_tasks,"Task_count":Task_count})
    