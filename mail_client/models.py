import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    def create_user(self, mail_address, password=None, **extra_fields):
        if not mail_address:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(mail_address)
        user = self.model(mail_address=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mail_address, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(mail_address, password, **extra_fields)

class Connexion(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mail_address = models.EmailField(max_length=320, unique=True, null=False)
    domaine = models.CharField(max_length=255, null=False)
    port = models.IntegerField(null=False)
    password = models.CharField(max_length=128, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'mail_address'
    REQUIRED_FIELDS = ['domaine', 'port']

    def __str__(self):
        return self.mail_address

    def get_full_name(self):
        return self.mail_address

    def get_short_name(self):
        return self.mail_address