from rest_framework import serializers
from django.contrib import auth
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
class AuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    def authenticate(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            return Token.objects.get_or_create(user=user)

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
    def save_user(self, validated_data):
        user = User.objects.create_user(username=validated_data.get('username'), 
                                password=validated_data.get('password'), 
                                first_name=validated_data.get('first_name'), 
                                last_name=validated_data.get('last_name'), 
                                email=validated_data.get('email'))
        user.save()
