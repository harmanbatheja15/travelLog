from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.shortcuts import render, get_object_or_404
from ckeditor.fields import RichTextField

# Create your models here.

class MyAccountManager(BaseUserManager):

    def create_user(self, name, email, phone, password=None):
        if not email:
            raise ValueError("email is required!")
        user = self.model(
            name = name,
            phone = phone,
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, phone, password=None):
        user = self.create_user(
            name = name,
            phone = phone,
            email = self.normalize_email(email),
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = None
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=100, unique=True)
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)

    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    objects = MyAccountManager()

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

class Log(models.Model):

    visibility_choices = (
        ('public', 'public'),
        ('private', 'private'),
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateField()
    image = models.ImageField(upload_to='travelImages/')
    visibility = models.CharField(choices=visibility_choices, max_length=100)
    description = RichTextField()

    def __str__(self):
        return self.title

class LogImage(models.Model):
    log = models.ForeignKey(Log, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='travelImages/')
 
    def __str__(self):
        return self.log.title
