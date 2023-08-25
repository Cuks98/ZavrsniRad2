from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    role_id = models.IntegerField(null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['role_id']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Gym(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, blank=False, null=False)

class UserToGym(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    gym = models.ForeignKey('Gym', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'gym'], name='unique_user_gym')
        ]

class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    gym = models.ForeignKey('Gym', on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()