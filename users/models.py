from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import datetime


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=150, blank=True)
    fav_genre = models.CharField(max_length=50, blank=True)
    fav_author = models.CharField(max_length=150, blank=True)
    about_me = models.TextField(_(
        'about'), max_length=500, blank=True, null=True)
    genre = ArrayField(models.CharField(
        max_length=30), blank=True, null=True, size=10)
    state = models.CharField(max_length=60, blank=True)
    country = models.CharField(max_length=60, blank=True)
    image = models.ImageField(upload_to='images/', blank=True)
    catalogue = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    curr_reading = ArrayField(models.CharField(max_length=30), blank=True, null=True)
    readed = ArrayField(models.CharField(max_length=30), blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    login_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self):
        return self.user_name


class Comments(models.Model):
    bid = models.CharField(max_length=100)
    uid = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    body = models.TextField(max_length=800)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uid.user_name


class Likes(models.Model):
    bid = models.CharField(max_length=100)
    uid = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    liked = models.BooleanField()
    total_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.bid