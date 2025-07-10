from django.contrib.auth.models import AbstractUser
from django.db import models



# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('seller', 'Seller'),
    )

    username = models.CharField(
        ('username'),
        max_length=150,
        blank=True,
        null=True,
        unique=False
    )

    email = models.EmailField(('email address'), unique=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.email} ({self.role})"


# Permission Table
class Permission(models.Model):
    ACTION_CHOICES = (
        ('add', 'Add'),
        ('edit', 'Edit'),
        ('view', 'View'),
        ('delete', 'Delete'),
    )

    name = models.CharField(max_length=50)  # e.g., 'product', 'order'
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)

    class Meta:
        unique_together = ('name', 'action')

    def __str__(self):
        return f"{self.action.upper()} {self.name.capitalize()}"

# RolePermission Table
class RolePermission(models.Model):
    role = models.CharField(max_length=10, choices=User.ROLE_CHOICES)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.upper()} can {self.permission}"



def has_permission(user, action, resource):
    return RolePermission.objects.filter(
        role=user.role,
        permission__name=resource,
        permission__action=action
    ).exists()
