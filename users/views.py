from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from users.forms import RegisterForm,CustomRegistrationForm
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
# Create your views here.
def sign_up(request):
      if request.method == 'GET':
         form=CustomRegistrationForm()
      if request.method == 'POST':
          form=CustomRegistrationForm(request.POST)
          if form.is_valid():
              user=form.save(commit=False)
              user.set_password(form.cleaned_data.get('password1'))
              user.is_active=False
              user.save()
              messages.success(request, "A Confirmation mail was Sent check your Email")
              return redirect('sign-in')
            #   username=form.cleaned_data.get('username')
            #   password=form.cleaned_data.get('password1')
            #   confirm_password=form.cleaned_data.get('password2')
              
            #   if password == confirm_password:
            #       User.objects.create(username=username,password=password)
          else:
              messages.error(request, "Invalid,please Try Again !")
              print("password do not match")
      return render(request, 'registration/register.html',{'form':form})
 
def  sign_in(request):
    form=LoginForm()
    if request.method == 'POST':
      form=LoginForm(data=request.POST)
      if form.is_valid():
         user=form.get_user()
         login(request,user)
         return redirect('home')  
    return render(request, 'registration/login.html',{'form':form})

def sign_out(request):
  if request.method == 'POST':
    logout(request)
  return redirect('sign-in')

def activate_user(request,user_id,token):
  try: 
      user= User.objects.get(id=user_id)
      if default_token_generator.check_token(user,token):
         user.is_active=True
         user.save()
         return redirect('sign-in')
      else:
        user.is_active=False
        return HttpResponse('Invalid ID or token')
  except User.DoesNotExist:
    return HttpResponse('User not found')
     