from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Student(models.Model):
    StudentName=models.CharField(max_length=30)
    StudentPassword=models.CharField(max_length=30)
    StudentClass=models.CharField(max_length=30)

    def __str__(self):
        return self.StudentName

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def create_superuser(self, name,email,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            name,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
