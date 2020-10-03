from django.contrib import admin
from .models import Task, List
from django.contrib import messages 
class TaskAdmin(admin.ModelAdmin): 
    list_display = ('title', 'deadline', 'complete')
    def complete(self, request, queryset): 
        queryset.update(complete = 1) 
        messages.success(request, "Selected Record(s) marked as complete.")
    def incomplete(self, request, queryset): 
        queryset.update(complete = 0) 
        messages.success(request, "Selected Record(s) marked as incomplete.") 
    admin.site.add_action(complete, "Mark Complete")
    admin.site.add_action(incomplete, "Mark Incomplete") 

admin.site.register(Task)
admin.site.register(List)
# Register your models here.

