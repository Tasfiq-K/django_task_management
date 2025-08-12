from django.urls import path
from . import views

app_name = 'task_management_system_app'

urlpatterns = [
    # path('', views.user_login, name='login'),
    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    # path('logout/', views.user_logout, name='logout'),
    path('user/', views.user_tasks_list, name='user_tasks_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/update/<int:task_id>/', views.update_task, name='update_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/<int:category_id>/', views.category_tasks, name='category_tasks'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('task-chart/', views.task_chart, name='task_chart'),
    path('tasks/<int:task_id>/comment/', views.add_comment, name='add_comment'),
]