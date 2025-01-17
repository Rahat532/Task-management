from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
   return HttpResponse("Welcome to the Task Management System!")

def contact(request):
    return HttpResponse("<h1 style='color:blue'>Contact us at support@taskmanagement.com</h1>")

def show_task(request):
    return HttpResponse("This is Our Task page!")

def show_specific_task(request,id):
    print("Id : ",id)
    print("ID type: ", type(id))
    return HttpResponse(f"This is Your Specific Task page! numebers{id}")                              