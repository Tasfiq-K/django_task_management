from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def user_tasks_list(request):
    tasks = request.user.tasks.all()
    return render(request, 'user_dashboard/dashboard.html', {'tasks': tasks})