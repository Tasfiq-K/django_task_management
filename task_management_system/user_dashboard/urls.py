from django.urls import path
from . import views

app_name = "user_dashboard"

urlpatterns = [
    path('user/', views.user_tasks_list, name='user_tasks_list'),

   ]