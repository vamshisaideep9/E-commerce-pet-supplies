from django.db import models
from django.contrib.auth import get_user_model
from users.models import UserProfile
from products.models import Product

User = get_user_model()

# Create your models here.


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    earned_points = models.IntegerField(default=0)


    def save(self, *args, **kwargs):
        if self.earned_points == 0:
            self.earned_points = int(float(self.total_price) * 0.1)
            user_profile, created = UserProfile.objects.get_or_create(user=self.user)
            user_profile.loyality_points += self.earned_points
            user_profile.save()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Order {self.id} - {self.status}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order {self.order.id}"
