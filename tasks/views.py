from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, TaskGroup
from .forms import TaskForm

def index(request):
    return render(request, 'index.html', {"name": "World"})


def task_list(request):
    tasks = Task.objects.all()
    taskgroups = TaskGroup.objects.all()
    ctx = { "task_list": tasks, "taskgroups":taskgroups }

    if request.method == "POST":
        t = Task()
        t.name = request.POST.get('task_name')
        t.due_date = request.POST.get('due_date')
        t.taskgroup = TaskGroup.objects.get(pk=request.POST.get('taskgroup'))
        t.save()

    return render(request, 'task_list.html', ctx)


def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    ctx = { "task": task }
    return render(request, 'task_detail.html', ctx)


class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['taskgroups'] = TaskGroup.objects.all()
        context['form'] = TaskForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()

        return self.get(request, *args, **kwargs)


class TaskDetailView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_detail.html'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_detail.html'


# class TaskListView(TemplateView):
    # template_name = 'task_list.html'

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['tasks'] = tasks
        # return context

    # def post(self, request, *args, **kwargs):
        # tasks.append(request.POST.get('task_name'))
        # return self.get(request, *args, **kwargs)
