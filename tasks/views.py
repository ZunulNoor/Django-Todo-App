import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

USERS_FILE = 'user.txt'
TASKS_FILE = 'task.txt'

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')
    return render(request, 'tasks/signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('todo')
    return render(request, 'tasks/login.html')

def todo_view(request):
    if request.user.is_authenticated:
        tasks = []
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as f:
                for line in f:
                    email, title, description = line.strip().split(',')
                    if email == request.user.email:
                        tasks.append({'title': title, 'description': description})
        return render(request, 'tasks/todo.html', {'tasks': tasks, 'email': request.user.email})
    return redirect('login')

def create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        with open(TASKS_FILE, 'a') as f:
            f.write(f'{request.user.email},{title},{description}\n')
        return redirect('todo')
    
def edit_task(request, task_title):
    if request.method == 'POST':
        new_title = request.POST['title']
        new_description = request.POST['description']
        tasks = []

        # Read existing tasks
        with open(TASKS_FILE, 'r') as f:
            tasks = f.readlines()

        # Write updated tasks
        with open(TASKS_FILE, 'w') as f:
            for line in tasks:
                if line.startswith(f"{request.user.email},{task_title}"):
                    f.write(f"{request.user.email},{new_title},{new_description}\n")  # Update task
                else:
                    f.write(line)  # Keep existing tasks

        return redirect('todo')

def delete_task(request, task_title):
    if request.method == 'POST':
        # Logic to delete a task
        # This is a basic example; a better approach would be to handle task IDs
        tasks = []
        with open(TASKS_FILE, 'r') as f:
            tasks = f.readlines()
        with open(TASKS_FILE, 'w') as f:
            for line in tasks:
                if not line.startswith(f"{request.user.email},{task_title}"):
                    f.write(line)
        return redirect('todo')
