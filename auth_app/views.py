from django.contrib.auth import authenticate
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import StudentSerializer,RegisterSerializer
from .models import Student,User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication,JWTTokenUserAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import reverse
from django.shortcuts import render, redirect, HttpResponseRedirect


ACCESS_TOKEN_GLOBAL=None
class Register(APIView):
    RegisterSerializer_Class=RegisterSerializer
    def get(self,request):
        return render(request, 'register.html')
    def post(self,request,format=None):
        serializer=self.RegisterSerializer_Class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg={
                'msg':"Registered Successfully"
            }
            return render(request, 'login.html',msg)
        else:
            return Response({"Message":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})

class Login(APIView):
    def get(self,request):
        if 'logged_in' in request.COOKIES and 'Access_Token' in request.COOKIES:
            context = {
                'Access_Token': request.COOKIES['Access_Token'],
                'logged_in': request.COOKIES.get('logged_in'),
            }
            return render(request, 'abc.html', context)
        else:
            return render(request, 'login.html')

    def post(self,request,format=None):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')


        refresh = RefreshToken.for_user(user)
        global ACCESS_TOKEN_GLOBAL
        ACCESS_TOKEN_GLOBAL=str(refresh.access_token)
        print("ACCESS_TOKEN_GLOBAL in login=> ",ACCESS_TOKEN_GLOBAL)
        response=render(request,'students.html')
        response.set_cookie('Access_Token',ACCESS_TOKEN_GLOBAL)
        response.set_cookie('logged_in', True)
        return response

class StudentData(APIView):
    authentication_classes=[JWTAuthentication,]

    StudentSerializer_Class=StudentSerializer
    def get(self,request,format=None):

        token = request.COOKIES.get('Access_Token')
        print("ACCESS_TOKEN_GLOBAL in stu=> ",ACCESS_TOKEN_GLOBAL)
        print("Access_Token in stu=> ",token)
        send='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQxMzI2NTUzLCJqdGkiOiI4Mjk1OGYwZTA2NjM0YmU1OTM5ODhhNjhkMzY1NWJlZSIsInVzZXJfaWQiOjF9.PrYE9pvkuHaaZnq9HkdnfSLpkz6B8MtPcMik4pu8ChY'
        if token!=ACCESS_TOKEN_GLOBAL and token==None:
            raise AuthenticationFailed('Unauthenticated!')
        DataObj=Student.objects.all()
        serializer=self.StudentSerializer_Class(DataObj,many=True)
        serializerData=serializer.data
        return Response(
    {
        "message": "Login Successfully",
        "code": "HTTP_200_OK",
        "user": serializerData
    }
)

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

            response = HttpResponseRedirect(reverse('login'))

            # deleting cookies
            response.delete_cookie('Access_Token')
            response.delete_cookie('logged_in')

            return response
        except:
            return Response({"status":status.HTTP_400_BAD_REQUEST})
