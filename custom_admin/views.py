from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import login_serializer, user_list_serializer, create_user_serializer, user_update_serializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from user.models import User
from django.contrib.auth.hashers import make_password


class login(APIView):
    serializerclass = login_serializer
    

    def post(self, request, format=None):
        """
        authenticating admin user explicitly and tocken and refresh tocken is generated and 
        provided for a valied user
        """
        
        # vallidating login credencials
        # if eny exception found in the validation
        # if excepton found, error message implicitly send to the frontend, becouse raise_exception=True.
        serialized_data = self.serializerclass(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            
            # fetching validated data
            username = serialized_data.validated_data['username']
            password = serialized_data.validated_data['password']
            
        
        # authenticating user
        user = authenticate(username = username, password = password)
        if user and user.is_superuser:
            """
            if the user is authenticated superuser, a refresh tocken and access tocken generated
            and send back to the user along with the user credecials
            """
            
            # generating jwt refresh and access tocken for the loged in user
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            
            # return the credencials to the frontend
            return_data = {
                'user' : serialized_data.validated_data['username'],
                'refresh' : str(refresh),
                'access' : str(access)
            }
            return Response(return_data, status=200)
        
        # invalied login credencials
        else:
            return Response({"message":"not authenticated"}, status=401)



# retreving users list
class users_list(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializerclass = user_list_serializer

    def get(self, request, format=None):
        
        # fetching user data
        user_list = User.objects.all()

        # serializing data and send to admin
        serialized_data = self.serializerclass(user_list, many = True)
        return Response(serialized_data.data, status=200)



# create new user
class add_user(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializerclass = create_user_serializer

    def post(self, request, format=None):
        
        serialized_data = self.serializerclass(data = request.data)

        if serialized_data.is_valid(raise_exception=True):
            """
            creating new user and return the data to the frond end with the newly created tocken
            password need to be explisitly hashed before call save(), save() doesnt shash password 
            """

            # password hashing, save() method doest hash password
            hashed_password = make_password(serialized_data.validated_data['password'])
            
            try:
                serialized_data.save(password = hashed_password)
                print("user created")
            except Exception as e:
                print(e)
                return Response({"message":"user creation error"},status=403)

            return Response({"username":serialized_data.validated_data['username'], "first_name":serialized_data.validated_data.get('first_name')}, status=201)
        

# delete user
class delete_user(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def delete(self, request, user_id, format=None):
        """
        fetching username from the url and finding the matching user 
        and perform delete query
        """

        # deleting user
        try:
            User.objects.get(id = user_id).delete()

        # any exception
        except Exception as e:
            print(e)
            return Response({"details":"can't delete, exception found while delete"}, status=403)

        return Response({"details":"user deleted"}, status=200)



# update user
class update_user(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializerclass = user_update_serializer

    def patch(self, request, format=None):
        """
        this is fetching optional updation data and serialize it using model serializer
        if the serialized data is valied, procede to updating the fields
        user id is mandatory to find the user to update
        """

        # checking the user using id
        try:
            user_obj = User.objects.get(id = request.data.get('id'))
        
        # return exceptons if user not found or id not given
        except Exception as e:
            print(e)
            return Response({"data":"user not found"})
        
        # partial is set to true, to neglect the empty feld, becouse only provided data can be updated
        serialized_data = self.serializerclass(user_obj,data=request.data, partial = True)
        
        # update new data if data is valiedated
        # any exception found, is_valid fucntion rise exceton and send back to user implicitly
        if serialized_data.is_valid(raise_exception=True):

            # save data and return updated data
            serialized_data.save()
            return Response(serialized_data.data, status=200)
        


        
