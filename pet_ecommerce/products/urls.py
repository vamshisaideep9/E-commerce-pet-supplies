from django.urls import path
from .views import CategoryListCreateView, ProductListView, ProductCreateView, ProductDetailView

urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/create/", ProductCreateView.as_view(), name="product-create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
]
