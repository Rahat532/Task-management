from django.contrib import admin
from tasks.models import Tasks,TaskDetail,Employee,Project

# Register your models here.
admin.site.register(Tasks)
admin.site.register(TaskDetail)
admin.site.register(Employee)
admin.site.register(Project)