from django.db import models

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='brand_images/')

    class Meta:
        db_table="brand_table"

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='vehicle_images/')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,related_name='vehicle_brand')

    class Meta:
        db_table="vehicle_table"

class Category(models.Model):
    image = models.ImageField(upload_to='category_images/')
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "category_table"


class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='product_vehicle')
    highlights = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table="product_table"



