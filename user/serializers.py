from rest_framework import serializers
from .models import User

class user_serializer(serializers.ModelSerializer):  

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name']
        

class login_serializer(serializers.Serializer):

    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)


class update_serializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
