# from django.shortcuts import render, redirect
# from google.oauth2 import credentials
# from google_auth_oauthlib.flow import Flow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build
# from .models import CustomUser
# from random_contacts_project import settings

# def google_authenticate(request):
#     flow = Flow.from_client_secrets_file(
#         settings.GOOGLE_CLIENT_SECRET_FILE,
#         scopes=settings.GOOGLE_SCOPES,
#         redirect_uri=request.build_absolute_uri('/google-auth-callback')
#     )

#     # Redirect the user to Google for authentication
#     authorization_url, state = flow.authorization_url(
#         access_type='offline',
#         include_granted_scopes='true'
#     )
#     request.session['state'] = state
#     return redirect(authorization_url)

# def get_user(id_):
#     try:
#         return CustomUser.objects.get(pk=id_) # <-- tried to get by email here
#     except CustomUser.DoesNotExist:
#         return None
    
# def google_auth_callback(request):
#     state = request.session.get('state', '')
#     flow = Flow.from_client_secrets_file(
#         settings.GOOGLE_CLIENT_SECRET_FILE,
#         scopes=settings.GOOGLE_SCOPES,
#         redirect_uri=request.build_absolute_uri('/google-auth-callback'),
#         state=state
#     )

#     # Fetch the access token
#     flow.fetch_token(authorization_response=request.build_absolute_uri())
#     credentials = flow.credentials
#     print(credentials.__dict__)
#     print(request)
#     print("sdfghjikopghjkl")
#     print(request.user)
#     user_id = request.user.id
#     custom_user = CustomUser.objects.get(id=user_id)
#     custom_user.google_credentials = credentials.to_json()
#     custom_user.save()

#     return redirect('contacts')

# def contacts(request):
#     user_id = request.user.id
#     custom_user = CustomUser.objects.get(id=user_id)
#     credentials = credentials.Credentials.from_json(custom_user.google_credentials)

#     # Check if the access token is expired and refresh if necessary
#     if credentials.expired:
#         if credentials.refresh_token:
#             credentials.refresh(Request())
#         else:
#             return redirect('google-auth')

#     # Build the Google Contacts API service
#     service = build('people', 'v1', credentials=credentials)
#     contacts = service.people().connections().list(
#         resourceName='people/me',
#         pageSize=10,
#         personFields='names,emailAddresses',
#         sortOrder='LAST_MODIFIED_DESCENDING'
#     ).execute().get('connections', [])

#     context = {
#         'contacts': contacts
#     }
#     return render(request, 'contacts.html', context)


# # from django.shortcuts import render, redirect
# # from django.contrib.auth import authenticate, login
# # from google.oauth2 import credentials
# # from google_auth_oauthlib.flow import Flow
# # from google.auth.transport.requests import Request
# # from googleapiclient.discovery import build
# # from .models import CustomUser

# # def google_authenticate(request):
# #     flow = Flow.from_client_secrets_file(
# #         settings.GOOGLE_CLIENT_SECRET_FILE,
# #         scopes=settings.GOOGLE_SCOPES,
# #         redirect_uri=request.build_absolute_uri('/google-auth-callback')
# #     )

# #     # Redirect the user to Google for authentication
# #     authorization_url, state = flow.authorization_url(
# #         access_type='offline',
# #         include_granted_scopes='true'
# #     )
# #     request.session['state'] = state
# #     return redirect(authorization_url)

# # def google_auth_callback(request):
# #     state = request.session.get('state', '')
# #     flow = Flow.from_client_secrets_file(
# #         settings.GOOGLE_CLIENT_SECRET_FILE,
# #         scopes=settings.GOOGLE_SCOPES,
# #         redirect_uri=request.build_absolute_uri('/google-auth-callback'),
# #         state=state
# #     )

# #     # Fetch the access token
# #     flow.fetch_token(authorization_response=request.build_absolute_uri())
# #     credentials = flow.credentials

# #     # Check if the user already exists
# #     user = authenticate(request, credentials=credentials)
# #     if user is None:
# #         # Create a new user if the user doesn't exist
# #         print(credentials.__dict__)
# #         user = CustomUser.objects.create_user(username=credentials.id_token['email'])
# #         user.google_credentials = credentials.to_json()
# #         user.save()

# #     login(request, user)

# #     return redirect('contacts')





from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView
from .utils import get_tokens_for_user
from .serializers import RegistrationSerializer, PasswordChangeSerializer


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
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
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




