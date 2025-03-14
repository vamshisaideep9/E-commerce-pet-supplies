from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer, UserProfileSerializer
from users.models import UserProfile
from rest_framework.decorators import api_view, permission_classes
from products.models import Product
from reportlab.pdfgen import canvas


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    



    def create(self, request, *args, **kwargs):
        user = request.user
        items = request.data.get("items", [])


        if not items:
            return Response({"error": "Order must contain at least one item."}, status=status.HTTP_400_BAD_REQUEST)
        

        order = Order.objects.create(user=user)
        total_price = 0
        order_items = []

        for item in items:
            product_id = item.get("product")
            quantity = item.get("quantity", 1)


            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
            

            
            if quantity > product.stock: 
                return Response({"error": f"Not enough stock for {product.name}. Only {product.stock} left."}, status=status.HTTP_400_BAD_REQUEST)    
            

            price = product.price * quantity
            total_price += price
            product.stock -= quantity
            product.save()

            order_items.append(OrderItem(order=order, product=product, quantity=quantity, price=price))

        OrderItem.objects.bulk_create(order_items)   
        order.total_price = total_price
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)




class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)



class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


import logging  
logger = logging.getLogger(__name__)
from django.http import HttpResponse

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def generate_order_receipt(request, order_id):
    user = request.user
    logger.info(f"User {user} requested receipt for Order ID {order_id}")

    try:
        order = Order.objects.get(id=order_id, user=user)
        logger.info(f"Order found: {order}")
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found for user {user}")
        return Response({"error": "Order not found or not paid"}, status=404)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="order_{order.id}_receipt.pdf"'

    pdf = canvas.Canvas(response)
    pdf.setTitle(f"Order Receipt #{order.id}")

    pdf.drawString(100, 800, f"Order Receipt #{order.id}")
    pdf.drawString(100, 780, f"Date: {order.created_at.strftime('%Y-%m-%d')}")
    pdf.drawString(100, 760, f"Total Amount: ₹{order.total_price}")

    y_position = 740
    order_items = order.items.all()
    logger.info(f"Order {order_id} has {len(order_items)} items.")

    for item in order_items:
        logger.info(f"Adding item to PDF: {item.product.name}, Qty: {item.quantity}, Price: {item.price}")
        pdf.drawString(100, y_position, f"{item.product.name} - {item.quantity} x ₹{item.price}")
        y_position -= 20

    pdf.showPage()
    pdf.save()
    logger.info(f"PDF generated successfully for Order {order_id}")

    return response



class loyalityPointsView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]
    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def redeem_points(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if user_profile.loyality_points < 100:
        return Response({"error": "Not enough points to redeem"}, status=400)

    discount = user_profile.loyality_points // 100 * 10  # 100 points = ₹10
    user_profile.loyality_points %= 100  # Deduct redeemed points
    user_profile.save()

    return Response({"message": f"You have redeemed points for ₹{discount} discount", "remaining_points": user_profile.loyalty_points})

