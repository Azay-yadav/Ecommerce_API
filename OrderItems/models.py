from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import Product
from Orders.models import Order



# Order Item Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderItems_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orderItems_product')
    quantity = models.PositiveIntegerField(default=1)
    price_at_order_time = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} (Order #{self.order.id})"
