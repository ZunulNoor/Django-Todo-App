from django.urls import path
from .views import signup, user_login, todo_view, create_task, delete_task,edit_task

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('todo/', todo_view, name='todo'),
    path('create-task/', create_task, name='create_task'),
    path('delete-task/<str:task_title>/', delete_task, name='delete_task'),
    path('edit-task/<str:task_title>/', edit_task, name='edit_task'),
]
