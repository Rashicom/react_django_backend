from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import user_serializer, login_serializer, update_serializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import address, User
from rest_framework.permissions import IsAuthenticated, AllowAny


# signup
class signup(APIView):
    serializerclass = user_serializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """
        serializing the data and creating new using if the data is 
        validated 
        """
        
        # serializing the data
        serialized_data = self.serializerclass(data = request.data)
        
        # if is_valied rise any exceptions it automatically return error to the frontend
        # we dond want to explicitly send the error, for send erro explicitly set raise_excepton = False
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
 


# user login
class login(APIView):
    serializerclass = login_serializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """
        authenticating user explicitly and tocken and refresh tocken is generated and 
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
        if user:
            """
            if the user is authenticated, a refresh tocken and access tocken generated
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



# update image
class update_image(APIView):
    permission_classes = [IsAuthenticated]
    serializerclass = update_serializer

    def patch(self, request, format=None):
        """
        updating given info
        """
        
        # fetch the user data using id
        try:
            user_obj = User.objects.get(id = request.data.get('id'))

        # if exception found return exception back
        except Exception as e:
            print(e)
            return Response({"details":"user not found"})

        # serializing and updating data if data is valied
        serialized_data = self.serializerclass(user_obj, data = request.data, partial = True)
        if serialized_data.is_valid(raise_exception=True):
            """
            if the data is valied it is saved and updated data is returned
            """

            serialized_data.save()
            return Response({"details":"updated"}, status=201)
                    
        



# home page
class home(APIView):
    permission_classes = [IsAuthenticated]
    serializerclass = update_serializer

    def get(self, request, format=None):
        print("autherized user")
        user = User.objects.get(username=request.user)
        print(user)
        
        serialized_data = self.serializerclass(user)
        return Response(serialized_data.data,status=200)




        