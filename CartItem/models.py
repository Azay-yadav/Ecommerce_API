from django.db import models
from Users.models import User
from products.models import Product

# Create your models here.
# Cart Item Model
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cartItem_user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartItem_product')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} (User: {self.user.username})"
