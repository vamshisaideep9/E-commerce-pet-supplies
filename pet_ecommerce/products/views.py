from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from users.permissions import IsAdmin, IsVendor

# Create your views here.

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin | IsVendor]



class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendor]


    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)



class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendor]


    def get_queryset(self):
        if self.request.user.role == "vendor":
            return Product.objects.filter(created_by=self.request.user)
        return Product.objects.none()
