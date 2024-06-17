from django.db import models
from spare_part_app.models import *

class User(models.Model):
    user_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=12)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "user_table"

class Address(models.Model):
    address_id=models.AutoField(primary_key=True)
    user_id= models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    address = models.TextField()
    pin_code = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "address_table"

class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    user_id= models.ForeignKey(User, on_delete=models.CASCADE)
    product_id= models.ForeignKey(Product, on_delete=models.CASCADE)
    address_id=models.ForeignKey(Address,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    total=models.IntegerField()
    payment_method=models.CharField(max_length=100)

    class Meta:
        db_table = "order_table"











