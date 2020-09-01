from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import List, Task
from .forms import TaskForm, ListForm
from django.urls import reverse_lazy, reverse
class Home(LoginRequiredMixin, View):
    def get(self, request):
        _lists = List.objects.filter(user=request.user)
        incomplete_tasks = Task.objects.filter(_list__user=request.user).filter(complete=False).exclude(deadline__isnull=True).order_by('deadline')
        complete_tasks = Task.objects.filter(_list__user=request.user).filter(complete=True).exclude(deadline__isnull=True).order_by('deadline')
        context = {'list':_lists, 'incomplete_tasks':incomplete_tasks, 'complete_tasks':complete_tasks}
        return render(request, 'TaskManager/home.html', context)

class ListCreate(LoginRequiredMixin, CreateView):
    form_class = ListForm
    template_name = 'TaskManager/list_form.html'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
class ListDetails(LoginRequiredMixin, DetailView):
    model = List
    template_name = "TaskManager/list_details.html"
    def get_queryset(self, **kwargs):
        qs = List.objects.filter(id=self.kwargs['pk'])
        if self.request.user == qs[0].user:
            return qs
        return qs.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        incomplete_tasks = Task.objects.filter(_list=context['list']).filter(complete=False).order_by('deadline')
        complete_tasks = Task.objects.filter(_list=context['list']).filter(complete=True).order_by('deadline')
        context['incomplete_tasks'] = incomplete_tasks
        context['complete_tasks'] = complete_tasks
        return context
class ListUpdate(LoginRequiredMixin, UpdateView):
    form_class = ListForm
    template_name = 'TaskManager/list_form.html'
    success_url = reverse_lazy('home')
    def get_queryset(self, **kwargs):
        qs = List.objects.filter(id=self.kwargs['pk'])
        if self.request.user == qs[0].user:
            return qs
        return qs.none()
class ListDelete(LoginRequiredMixin, DeleteView):
    model = List
    success_url = reverse_lazy('home')


# class ListDetails(LoginRequiredMixin, View):
#     def get(self, request, list_id):
#         l = List.objects.get(id=list_id)
#         if l.user != request.user:
#             return HttpResponse("No pls")
#         incomplete_tasks = Task.objects.filter(_list=l).filter(complete=False).order_by('deadline')
#         complete_tasks = Task.objects.filter(_list=l).filter(complete=True).order_by('deadline')
#         context = {'list':l, 'incomplete_tasks':incomplete_tasks, 'complete_tasks':complete_tasks}
#         return render(request, 'TaskManager/list_details.html', context)

class ToggleComplete(LoginRequiredMixin, View):
    def post(self, request):
        task = Task.objects.filter(id=request.POST['task_id'])
        response = HttpResponse("No pls")
        if task.exists():
            task = task[0]
            if task._list.user == request.user:
                task.complete = not task.complete
                task.save()
                response = HttpResponse(task.complete)
        return response

class AddTask(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = "TaskManager/task_form.html"
    def form_valid(self, form):
        _list = List.objects.get(id=self.kwargs['list_id'])
        if _list.user == self.request.user:
            form.instance._list = _list
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('list_details', kwargs={'pk':self.kwargs['list_id']})

# class AddTask(LoginRequiredMixin, View):
#     def get(self, request, list_id):
#         _list = List.objects.get(id=list_id)
#         if _list.user != request.user:
#             return HttpResponse("No pls")
#         form = TaskForm()
#         context = {'form': form}
#         return render(request, 'TaskManager/task_form.html', context)
#     def post(self, request, list_id):
#         _list = List.objects.get(id=list_id)
#         if _list.user != request.user:
#             return HttpResponse("No pls")
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             new_task = form.save(commit=False)
#             new_task._list = _list
#             new_task.save()
#             return redirect(reverse_lazy('list_details', kwargs={'list_id':list_id}))
#         else:
#             return render(request, 'TaskManager/task_form.html', {'form':form})

class DeleteTask(LoginRequiredMixin, DeleteView):
    pass