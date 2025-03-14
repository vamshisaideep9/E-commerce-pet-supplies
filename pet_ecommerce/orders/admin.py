from django.contrib import admin
from .models import Order, OrderItem
from users.models import UserProfile

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "created_at", "earned_points")
    list_filter = ("created_at", )
    search_fields = ("user__username",)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "loyality_points")
    search_fields = ("user__username",)
