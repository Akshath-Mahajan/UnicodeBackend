from rest_framework import serializers
from ..models import List, Task

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['name', 'user']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['_list', 'title', 'description', 'deadline', 'complete', 'date_complete']