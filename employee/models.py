from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError 

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance) 

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    active = models.BooleanField(default=True)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  

    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

def validate_aadhar(value):
    if len(value) != 12:
        raise ValidationError(
            "Enter a valid aadhar number",
            params={'value': value},
        )


# def validate_contact(value):
#     if len(value) != 10:
#         raise ValidationError(
#             "Enter a valid contact number",
#             params={'value': value},
#         )

class Employee(models.Model):
    photo=models.ImageField(upload_to='profilepic',null=True)
    name=models.CharField(max_length=100)
    employee_code=models.CharField(max_length=100,unique=True)
    address=models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = PhoneNumberField(
        ('phone number'),unique=True, null=True,
        blank=True,
        error_messages={
        ('unique'): ("A user with this phone number already exists."),
        },
    )
    DOB = models.DateField(null=True)
    aadharNumber = models.CharField(max_length=12,validators=[validate_aadhar])
    designation = models.CharField(max_length=100, null=True)
    bankName = models.CharField(max_length=50, null=True)
    ACNumber = models.CharField(max_length=50,null=True)
    branchName = models.CharField(max_length=50,null=True)
    IFSCNumber = models.CharField(max_length=50,null=True)
    salary=models.IntegerField(default=0)
