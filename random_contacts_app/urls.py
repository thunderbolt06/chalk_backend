from django.urls import path
from .views import Contacts, RegistrationView, LoginView, LogoutView, ChangePasswordView
from rest_framework_simplejwt import views as jwt_views

app_name = 'random_contacts_app'

urlpatterns = [
    path('accounts/register', RegistrationView.as_view(), name='register'),
    path('accounts/login', LoginView.as_view(), name='register'),
    path('accounts/logout', LogoutView.as_view(), name='register'),
    path('accounts/change-password', ChangePasswordView.as_view(), name='register'),
    path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('contacts', Contacts.as_view(), name='contacts'),
    path('contacts/top', Contacts.TopContacts.as_view(), name='contacts_top'),
]
