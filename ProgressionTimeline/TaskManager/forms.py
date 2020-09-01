from django import forms
from .models import Task, List

# Create the form class.
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline']
        widgets = {
            'title': forms.Textarea(attrs={'cols': 50, 'rows': 1, 'class':'form-control', 'placeholder':"Enter Title"}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 3, 'class':'form-control', 'placeholder':"Enter Description"}),
            'deadline': forms.DateTimeInput(attrs={'type':'date', 'class':'form-control', 'placeholder':"Enter Date"}),
        }
class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name']
        widgets={
            'name':forms.Textarea(attrs={'cols':25, 'rows':1, 'class':'form-control', 'placeholder':"Enter Name"})
        }