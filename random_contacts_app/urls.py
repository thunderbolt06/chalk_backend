# from django.urls import path
# from . import views

# urlpatterns = [
#     path('google-auth/', views.google_authenticate, name='google-auth'),
#     path('google-auth-callback/', views.google_auth_callback, name='google-auth-callback'),
#     path('contacts/', views.contacts, name='contacts'),
# ]


from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, ChangePasswordView
from rest_framework_simplejwt import views as jwt_views

app_name = 'random_contacts_app'

urlpatterns = [
    path('accounts/register', RegistrationView.as_view(), name='register'),
    path('accounts/login', LoginView.as_view(), name='register'),
    path('accounts/logout', LogoutView.as_view(), name='register'),
    path('accounts/change-password', ChangePasswordView.as_view(), name='register'),
    path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
