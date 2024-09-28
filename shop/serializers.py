from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    # Expect a product UUID instead of a nested product object
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(source="orderitem_set", many=True)

    class Meta:
        model = Order
        fields = ["id", "user", "created_at", "order_items", "total_price"]

    def create(self, validated_data):
        # Pop the order items data
        items_data = validated_data.pop("orderitem_set")
        
        # Create the order instance
        order = Order.objects.create(**validated_data)
        
        # Create order items associated with the order
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            
        return order
