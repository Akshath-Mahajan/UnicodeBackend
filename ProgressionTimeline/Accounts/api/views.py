from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.renderers import JSONRenderer
from .serializers import AuthenticationSerializer, SignupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            token, created = serializer.authenticate(serializer.data)
            return Response({"Token": token.key}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Signup(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save_user(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


