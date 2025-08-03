from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django import forms
from .models import Category, Task
from django.shortcuts import render, redirect
from .models import Category
from .models import Task
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import login_required


def is_admin(user):
    return user.is_superuser


# admin_required = user_passes_test(lambda user: user.is_superuser)
admin_required = user_passes_test(is_admin)


# Forms
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'category',
            'start_date',
            'end_date',
            'status',
            'description',
            'location',
            'organizer',
            'assigned_to'
        ]

        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['assigned_to'].queryset = User.objects.filter(id=user.id)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:  # If the user is an admin
                return redirect('category_list')
            else:  # If the user is a normal user
                return redirect('user_tasks_list')
    else:
        form = LoginForm()
    return render(request, 'task_management_system_app/login.html', {'form': form})


@login_required
def user_tasks_list(request):
    tasks = request.user.tasks.all()
    return render(request, 'task_management_system_app/user_tasks_list.html', {'tasks': tasks})




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'task_management_system_app/register.html', {'form': form})


def LogoutPage(request):
    logout(request)
    return redirect("login")


@login_required
@admin_required
def delete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.delete()
    return redirect(reverse('category_list'))


@login_required
# @admin_required
def create_task(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        # priority = request.POST.get('priority')
        status = request.POST.get('status')
        description = request.POST.get('description')
        location = request.POST.get('location')
        organizer = request.POST.get('organizer')
        assigned_to_id = request.POST.get('assigned_to')
        category = Category.objects.get(pk=category_id)
        task = Task.objects.create(
            name=name,
            category=category,
            start_date=start_date,
            end_date=end_date,
            # priority=priority,
            status=status,
            description=description,
            location=location,
            organizer=organizer,
            assigned_to_id=int(assigned_to_id)
        )

        if request.user.is_superuser:
            # Redirect to the task list page
            return redirect('category_list')
        else:
            return redirect('user_tasks_list')
    else:
        categories = Category.objects.all()
        users = User.objects.all()
        return render(request, 'task_management_system_app/create_task.html', {'categories': categories, 'users': users})


@login_required
# @admin_required
def update_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        # Update task fields based on form data
        task.name = request.POST.get('name')
        task.start_date = request.POST.get('start_date')
        task.end_date = request.POST.get('end_date')
        # task.priority = request.POST.get('priority')
        task.status = request.POST.get('status')
        task.description = request.POST.get('description')
        task.location = request.POST.get('location')
        task.organizer = request.POST.get('organizer')
        task.assigned_to_id = request.POST.get('assigned_to')
        task.save()
        return redirect('category_list')
    else:
        # Render update task page with task data
        return render(request, 'task_management_system_app/update_task.html', {'task': task})


@login_required
# @admin_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'task_management_system_app/category_list.html', {'categories': categories})


@login_required
@admin_required
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('category_list')
    return render(request, 'task_management_system_app/create_category.html')


@login_required
@admin_required
def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if category.task_set.exists():
        messages.error(
            request, "You cannot delete this category as it contains tasks.")
    else:
        category.delete()
        messages.success(request, "Category deleted successfully.")
    return redirect('category_list')


@login_required
@admin_required
def category_tasks(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    tasks = category.task_set.all()
    return render(request, 'task_management_system_app/category_tasks.html', {'category': category, 'tasks': tasks})


@login_required
@admin_required
def task_chart(request):
    categories = Category.objects.all()
    pending_counts = {}
    for category in categories:
        pending_counts[category.name] = Task.objects.filter(
            category=category,
            start_date__gt=timezone.now()
        ).count()
    return render(request, 'task_management_system_app/task_chart.html', {'pending_counts': pending_counts})