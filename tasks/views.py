from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TasksModelForm
from tasks.models import Employee,Tasks

# Create your views here.
def manager_dashboard(request):
    return render(request, 'dashboard/manager-dashboard.html')

def user_dashboard(request):
    return render(request, 'dashboard/user-dashboard.html')
def test(request):
    context={
        'names':["rahat","admin","user","manager"],
        'age':25,
    }
    return render(request, 'test.html', context)
def create_task(request):
    #employees= Employee.objects.all()
    form= TasksModelForm()# for Get Methods
    
    if request.method =="POST":
        form=TasksModelForm(request.POST)
        if form.is_valid():
            '''For Model From Data'''
            # print(form)
            form.save()
            
            return render(request,'task_from.html',{"form":form,"message":"Task added Successfully !"})
              
        '''For Django From Data'''
        #    data=form.cleaned_data
        #    title=data.get('title')
        #    description=data.get('description')
        #    due_date=data.get("due_date")
        #    assigned_to=data.get('assigned_to')# list
        #    task=Tasks.objects.create(title=title, description=description, due_date=due_date)
        # #    assign employee to Task
        # for emp_id in assigned_to:
        #     employee=Employee.objects.get(id=emp_id) 
        #     task.assigned_to.add(employee)
        #return HttpResponse("Task created successfully")
    context={"form": form}
    return render(request, 'task_from.html',context)