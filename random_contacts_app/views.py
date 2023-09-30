from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView
from .utils import get_tokens_for_user
from .serializers import ContactsSerializer, RegistrationSerializer, PasswordChangeSerializer, TopContactsSerializer
import json
from .models import Connection, Contact, MyUser

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        return Response("sdfhjk")

      
class LoginView(APIView):
    def post(self, request):
        if 'phone' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        phone = request.data.get("phone")
        password = request.data.get("password")
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

      
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


      
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True) #Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)





      
class ContactView(APIView):
    def post(self, request):
        isList = False
        if isinstance(request.data, list):
            isList = True
        serializer = ContactsSerializer(data=request.data, many=isList)
        if serializer.is_valid():
            serializer.create()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request):
        contacts = Contact.objects.all()
        return Response(contacts.values(), status=status.HTTP_200_OK)
    
    class TopContacts(APIView):
        def post(self, request):
            topContacts = Contact.objects.filter(fromPhone=request.data['fromPhone']).order_by('-dist')[:5]
            return Response(topContacts.values(), status=status.HTTP_200_OK)
        
class UserStatusView(APIView):
    def get(self, request):
        phone = request.query_params.get("phone")
        if MyUser.objects.filter(phone=str(phone)).exists():
            user = MyUser.objects.filter(phone=str(phone))
            return Response(getattr(user[0],"status"), status=status.HTTP_200_OK)
        return Response("Couldn't find user", status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        phone = request.query_params.get("phone")
        status1 = request.query_params.get("status")
        if MyUser.objects.filter(phone=str(phone)).exists():
            user = MyUser.objects.filter(phone=str(phone))
            user.update(status=status1)
            return Response("Success", status=status.HTTP_200_OK)
        
        return Response("Couldn't find user", status=status.HTTP_404_NOT_FOUND)
    
class ConnectionView(APIView):
    def get(self, request):
        fromPhone = request.query_params.get("fromPhone")
        status1 = request.query_params.get("status")
        a = Connection.objects.filter(fromPhone=fromPhone, status=status1).exists()
        b = Connection.objects.filter(toPhone=fromPhone, status=status1).exists()
        connection = object()
        if (a):
            connection = Connection.objects.filter(fromPhone=fromPhone, status=status1)
        elif (b):
            connection = Connection.objects.filter(toPhone=fromPhone, status=status1)
        else :
            return Response("Couldn't find user", status=status.HTTP_404_NOT_FOUND)
        return Response(getattr(connection[0], "toPhone"), status=status.HTTP_200_OK)

    def post(self, request):
        fromPhone = request.query_params.get("fromPhone")
        toPhone = request.query_params.get("toPhone")
        status1 = request.query_params.get("status")
        a = Connection.objects.filter(fromPhone=fromPhone, toPhone=toPhone).exists()
        b = Connection.objects.filter(toPhone=fromPhone, fromPhone=toPhone).exists()
        if a:
            connection = Connection.objects.filter(fromPhone=fromPhone, toPhone=toPhone)
            connection.update(isActive=status1)
        elif b:
            connection = Connection.objects.filter(toPhone=fromPhone, fromPhone=toPhone)
            connection.update(isActive=status1)
        else :
            connection = Connection(fromPhone=fromPhone, toPhone=toPhone, isActive=status1)
            connection.save()
        return Response("Sucess", status=status.HTTP_200_OK)
    
        
