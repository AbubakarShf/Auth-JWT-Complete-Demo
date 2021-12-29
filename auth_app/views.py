from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import StudentSerializer,RegisterSerializer
from .models import Student,User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
# Create your views here.

class Register(APIView):
    RegisterSerializer_Class=RegisterSerializer
    def post(self,request,format=None):
        serializer=self.RegisterSerializer_Class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":status.HTTP_200_OK,"Message":"Registered Successfully!"})
        else:
            return Response({"Message":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})
class Login(APIView):
    def post(self,request,format=None):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        refresh = RefreshToken.for_user(user)
        return Response({"status":status.HTTP_200_OK,"RefreshToken":str(refresh),"AccessToken":str(refresh.access_token)})


class StudentData(APIView):
    StudentSerializer_Class=StudentSerializer
    permission_classes=[IsAuthenticated,]
    def get(self,request,format=None):
        DataObj=Student.objects.all()
        serializer=self.StudentSerializer_Class(DataObj,many=True)
        serializerData=serializer.data
        print("HELLO=> ",serializerData)
        return Response({"status":status.HTTP_200_OK,"User":serializerData})
    def post(self,request,format=None):
        serializer=self.StudentSerializer_Class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializerData=serializer.data
            return Response({"status":status.HTTP_200_OK,"User":serializerData})
        else:
            return Response({"Message":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})

class Logout(APIView):
    def post(self,request):
        try:
            refersh_token=request.data.get('refresh_token')
            tokenObj = RefreshToken(refersh_token)
            tokenObj.blacklist()
            return Response({"status":status.HTTP_200_OK,"Message":"LOGOUT"})
        except:
            return Response({"status":status.HTTP_400_BAD_REQUEST})