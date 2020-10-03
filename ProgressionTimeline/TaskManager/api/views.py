from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from ..models import Task, List
from .serializers import ListSerializer, TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
class TaskCreate(APIView):
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['_list'].user == request.user:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'data': 'Not allowed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
@api_view(('GET',))
@renderer_classes([JSONRenderer])
def TaskDetail(request, pk):
    if request.method == 'GET':
        task = Task.objects.get(pk=pk)
        if task._list.user != request.user:
            return Response({'data': 'Not allowed'}, status.HTTP_400_BAD_REQUEST)
        serializer = TaskSerializer(task, many=False)
        return JsonResponse(serializer.data, safe=False)

class TaskUpdate(APIView):
    def get_object(self, pk, request):
        try:
            return Task.objects.get(pk=pk, _list__user=request.user)
        except Task.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        task = self.get_object(pk, request)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['_list'].user == request.user:
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'data': 'Not allowed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDelete(APIView):
    def get_object(self, pk, request):
        try:
            return Task.objects.get(pk=pk, _list__user=request.user)
        except Task.DoesNotExist:
            raise Http404
    def delete(self, request, pk, format=None):
        task = self.get_object(pk, request)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListCreate(APIView):
    def post(self, request, format=None):
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['user'] == request.user:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'data': 'Not allowed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
@api_view(('GET',))
@renderer_classes([JSONRenderer])
def ListDetail(request, pk):
    if request.method == 'GET':
        _list = List.objects.get(pk=pk)
        if _list.user != request.user:
            return Response({'data': 'Not allowed'}, status.HTTP_400_BAD_REQUEST)
        tasks = Task.objects.filter(_list=_list)
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)

class ListUpdate(APIView):
    def get_object(self, pk, request):
        try:
            return List.objects.get(pk=pk, user=request.user)
        except List.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        _list = self.get_object(pk, request)
        serializer = ListSerializer(_list, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['user'] == request.user:
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'data': 'Not allowed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListDelete(APIView):
    def get_object(self, pk, request):
        try:
            return List.objects.get(pk=pk, user=request.user)
        except List.DoesNotExist:
            raise Http404
    def delete(self, request, pk, format=None):
        _list = self.get_object(pk, request)
        _list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
