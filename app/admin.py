from django.contrib import admin
from .models import MyUSER,Restaurant,Customer,DeliveryPartner,MenuItem,Order,OrderItem,CartItem
# Register your models here.
admin.site.register(MyUSER)
admin.site.register(Restaurant)
admin.site.register(Customer)
admin.site.register(DeliveryPartner)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)