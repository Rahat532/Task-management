from django.urls import path
from tasks.views import manager_dashboard,employee_dashboard,test,create_task,view_task,update_task,delete_task

urlpatterns = [
    path('manager_dashboard/', manager_dashboard,name="Manager-Dashboard"),
    path('user_dashboard/', employee_dashboard),
    path('test/', test),
    path('create_task/', create_task,name="create-task"),
    path('show_task/', view_task),
    path('update-task/<int:id>/', update_task,name="update-task"),
    path('delete-task/<int:id>/',delete_task,name="delete-task"),
]
