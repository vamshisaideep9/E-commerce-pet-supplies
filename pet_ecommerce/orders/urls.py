from django.urls import path
from .views import OrderListCreateView, OrderDetailView, OrderHistoryView, generate_order_receipt, loyalityPointsView, redeem_points


urlpatterns = [
    path("orders/", OrderListCreateView.as_view(), name="order-list-create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("order-history/", OrderHistoryView.as_view(), name="order-history"),
    path("order-receipt/<int:order_id>/", generate_order_receipt, name="order-receipt"),
    path("loyalty-points/", loyalityPointsView.as_view(), name="loyalty-points"),
    path("redeem-points/", redeem_points, name="redeem-points"),
]
