from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name
    


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveBigIntegerField()
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name="products")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
