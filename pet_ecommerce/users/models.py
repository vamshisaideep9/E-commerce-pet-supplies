from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role="customer", **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        extra_fields.setdefault("role", role)  # Default role if not provided
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("vendor", "Vendor"),
        ("customer", "Customer"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="customer")
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, blank=True, null=True)  # Allow blank username

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No username required

    objects = UserManager()  # Use the custom UserManager




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    loyality_points = models.IntegerField(default=0)
