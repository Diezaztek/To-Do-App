from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

def sign_up(req):
    if req.method == 'GET':
        return render(req, 'tasks/signup.html', {'form':UserCreationForm()})
    else:
        username = req.POST['username']
        password = req.POST['password1']
        confirm_password = req.POST['password2']

        if password == confirm_password:
            try:
                user = User.objects.create_user(username, password=password)
                user.save()
                login(req, user)
                return redirect('tasks')

            except IntegrityError:
                return render(req, 'tasks/signup.html', {'form':UserCreationForm()
                                                        ,'error': 'El usuario ya existe, elige otro'})
        else:
            return render(req, 'tasks/signup.html', {'form':UserCreationForm()
                                                    ,'error': 'Las contraseñas no coinciden'})


def log_in(req):
    if req.method == 'GET':
        return render(req, 'tasks/login.html', {'form':AuthenticationForm()})
    else:
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req, username=username, password=password)
        if user is None:
            return render(req, 'tasks/login.html', {'form':AuthenticationForm()
                                                    ,'error': 'El usuario y la contraseña no coinciden'})
        else:
            login(req, user)
            return redirect('tasks') 

def log_out(req):
    if req.method == 'POST':
        logout(req)
        return redirect('home')


def go_home(req):
    return render(req, 'tasks/home.html')


def show_current_tasks(req):
    return render(req, 'tasks/tasks.html')
