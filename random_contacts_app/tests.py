from django.test import TestCase

# Create your tests here.

from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from .models import MyUser
from .views import RegistrationView

factory = APIRequestFactory()
user = MyUser.objects.get(email='asdfg@as.in')
view = RegistrationView.as_view()

# Make an authenticated request to the view...
request = factory.get('/accounts/login')
force_authenticate(request, user=user)
response = view(request)