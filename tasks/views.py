from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

@login_required
def log_out(req):
    if req.method == 'POST':
        logout(req)
        return redirect('home')


def go_home(req):
    return render(req, 'tasks/home.html')

@login_required
def show_current_tasks(req):
    tasks = Task.objects.filter(user = req.user, date_completed__isnull=True)
    return render(req, 'tasks/tasks.html', {'tasks': tasks})

@login_required
def create_task(req):
    if req.method == 'GET':
        return render(req, 'tasks/create.html', {'form':TaskForm()})
    else:
        try:
            form = TaskForm(req.POST)
            task = form.save(commit=False)
            task.user = req.user
            task.save()
            return redirect('tasks')
        except:
            return render(req, 'tasks/create.html', {'form':TaskForm()
                                                    ,'error': 'Datos no válidos'})
@login_required
def edit_task(req, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=req.user)

    if req.method == 'GET':
        form = TaskForm(instance=task)
        return render(req, 'tasks/edit.html', {'task':task, 'form':form})
    else:
        try:
            form = TaskForm(req.POST, instance=task)
            form.save()
            return redirect('tasks')
        except:
            return render(req, 'tasks/edit.html', {'task':task, 'form':form, 'error': 'Datos no válidos'})

@login_required
def complete_task(req, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=req.user)

    if req.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(req, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=req.user)

    if req.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def show_completed_tasks(req):
    tasks = Task.objects.filter(user = req.user, date_completed__isnull=False).order_by('-date_completed')
    return render(req, 'tasks/completed_tasks.html', {'tasks': tasks})
