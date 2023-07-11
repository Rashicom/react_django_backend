from rest_framework import serializers
from user.models import User


class login_serializer(serializers.Serializer):

    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    


class user_list_serializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class create_user_serializer(serializers.ModelSerializer):  

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name']


# for updating user data
class user_update_serializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'