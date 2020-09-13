from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import List, Task
from .forms import TaskForm, ListForm
from django.urls import reverse_lazy, reverse
from django.db import models
import datetime

class Home(LoginRequiredMixin, View):
    def get(self, request):
        _lists = List.objects.filter(user=request.user)
        incomplete_tasks = Task.objects.filter(_list__user=request.user).filter(complete=False).exclude(deadline__isnull=True).order_by('deadline')
        complete_tasks = Task.objects.filter(_list__user=request.user).filter(complete=True).exclude(deadline__isnull=True).order_by('deadline')
        context = {'list':_lists, 'incomplete_tasks':incomplete_tasks, 'complete_tasks':complete_tasks}
        response = render(request, 'TaskManager/home.html', context)
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response
class ListCreate(LoginRequiredMixin, CreateView):
    form_class = ListForm
    template_name = 'TaskManager/list_form.html'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        form.instance.user = self.request.user  #Make list owner as logged in user
        return super().form_valid(form)
class ListDetails(LoginRequiredMixin, DetailView):
    model = List
    template_name = "TaskManager/list_details.html"
    def get_queryset(self, **kwargs):
        qs = List.objects.filter(id=self.kwargs['pk'])
        if self.request.user == qs[0].user: #if list is owned by user
            return qs
        return qs.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        incomplete_tasks = Task.objects.filter(_list=context['list']).filter(complete=False).order_by('deadline')
        complete_tasks = Task.objects.filter(_list=context['list']).filter(complete=True).order_by('deadline')
        context['incomplete_tasks'] = incomplete_tasks
        context['complete_tasks'] = complete_tasks
        return context
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response
class ListUpdate(LoginRequiredMixin, UpdateView):
    form_class = ListForm
    template_name = 'TaskManager/list_form.html'
    success_url = reverse_lazy('home')
    def get_queryset(self, **kwargs):
        qs = List.objects.filter(id=self.kwargs['pk'])
        if self.request.user == qs[0].user: #if list is owned by user
            return qs
        return qs.none()
class ListDelete(LoginRequiredMixin, DeleteView):
    model = List
    success_url = reverse_lazy('home')

class ToggleComplete(LoginRequiredMixin, View):
    def post(self, request):
        task = Task.objects.filter(id=request.POST['task_id'])
        response = HttpResponse("No pls")
        now = datetime.datetime.now()
        if task.exists():
            task = task[0]
            if task._list.user == request.user: #if list is owned by user
                task.complete = not task.complete
                if task.complete:
                    task.date_complete = now
                else:
                    task.date_complete = None
                task.save()
                response = HttpResponse(task.complete)
        return response

class TaskCreate(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = "TaskManager/task_form.html"
    def form_valid(self, form):
        _list = List.objects.get(id=self.kwargs['pk'])
        if _list.user == self.request.user: #if list is owned by user
            form.instance._list = _list
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('list_details', kwargs={'pk':self.kwargs['pk']})

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('home')

class Timeline(LoginRequiredMixin, View):
    def get(self, request):
        tasks = []
        date = None
        if 'date' in request.GET:
            date = models.DateField().to_python(request.GET['date'])
            tasks = Task.objects.filter(_list__user=request.user, 
                                        date_complete__year=date.year,
                                        date_complete__month=date.month, 
                                        date_complete__day=date.day)
        ctx = {'tasks':tasks, 'date':date}
        return render(request, 'TaskManager/timeline.html', context=ctx)