
import datetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone


# Create your models here
class MyUserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given phone, date of
        birth and password.
        """
        if not phone:
            raise ValueError('Users must have an phone')

        user = self.model(
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        """
        Creates and saves a superuser with the given phone and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Contact(models.Model):
    fromPhone = models.CharField(max_length=255,)
    toPhone = models.CharField(max_length=255,)
    dist = models.IntegerField(default=0)
    def __str__(self):
        return self.fromPhone

class Connection(models.Model):
    fromPhone = models.CharField(max_length=255,)
    toPhone = models.CharField(max_length=255,)
    isActive = models.BooleanField(default=False)
    def __str__(self):
        return self.fromPhone

class MyUser(AbstractBaseUser):
    phone = models.CharField(
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        max_length=255,
        default="default"
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    credits = models.PositiveIntegerField(default=100)
    expiry_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(default="inactive", max_length=100)
    objects = MyUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_out_of_credits(self):
        "Is the user out  of credits?"
        return self.credits > 0

    @property
    def has_sufficient_credits(self, cost):
        return self.credits - cost >= 0

