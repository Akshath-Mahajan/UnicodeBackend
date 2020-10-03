from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from ..models import Task, List
from .serializers import ListSerializer, TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TaskCreate(APIView):
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
def TaskDetail(request, pk):
    if request.method == 'GET':
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task, many=False)
        return JsonResponse(serializer.data, safe=False)

class TaskUpdate(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDelete(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404
    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListCreate(APIView):
    def post(self, request, format=None):
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
def ListDetail(request, pk):
    if request.method == 'GET':
        tasks = Task.objects.filter(_list__id=pk)
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)

class ListUpdate(APIView):
    def get_object(self, pk):
        try:
            return List.objects.get(pk=pk)
        except List.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        _list = self.get_object(pk)
        serializer = ListSerializer(_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListDelete(APIView):
    def get_object(self, pk):
        try:
            return List.objects.get(pk=pk)
        except List.DoesNotExist:
            raise Http404
    def delete(self, request, pk, format=None):
        _list = self.get_object(pk)
        _list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
