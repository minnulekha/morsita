from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class MyUSER(AbstractUser):
    USER_TYPES = [
    ('customer', 'Customer'),
    ('restaurant', 'Restaurant Staff'),
    ('delivery', 'Delivery Partner'),
    ]
    usertype = models.CharField(max_length=20, choices=USER_TYPES)

class Restaurant (models.Model):
    restaurant_id=models.OneToOneField(MyUSER,on_delete=models.CASCADE)
    restaurant_name=models.CharField(max_length=255)
    owner_name=models.CharField(max_length=255)
    phone=models.CharField(max_length=15)
    address=models.CharField(max_length=255)
    pincode=models.IntegerField()
    logo=models.ImageField(upload_to='restaurant_logos/')

    def __str__(self):
        return self.restaurant_name

class Customer (models.Model):
    customer_id=models.OneToOneField(MyUSER,on_delete=models.CASCADE)
    phone=models.CharField(max_length=15)
    address=models.CharField(max_length=255)
    pincode=models.IntegerField()

    def __str__(self):
        return f"{self.customer_id.first_name} {self.customer_id.last_name}"
    
class DeliveryPartner (models.Model):
    deliverypartner_id=models.OneToOneField(MyUSER,on_delete=models.CASCADE)
    phone=models.CharField(max_length=15)
    vehicle_number=models.CharField(max_length=15)
    address=models.CharField(max_length=255)
    is_available=models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.deliverypartner_id.first_name} {self.deliverypartner_id.last_name}"
    
class MenuItem (models.Model):
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    item_name=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    item_image=models.ImageField(upload_to='menu_images/')
    category=models.CharField(max_length=255)
    is_available=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.item_name}({self.restaurant.restaurant_name})"
    
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    delivery_partner = models.ForeignKey(DeliveryPartner, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.customer}"

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.item_name} x{self.quantity}"

class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.menu_item.item_name} x{self.quantity} for {self.customer.customer_id.username}"

    def get_total_price(self):
        return self.quantity * self.menu_item.price

