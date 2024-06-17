from django.db import models
from django.contrib.auth.hashers import check_password,make_password

class User(models.Model):
    user_id=models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=12)
    email = models.EmailField(max_length=100, unique=True)
    phone_number=models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)


    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    class Meta:
        db_table = "users_table"

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

# Vehicle related models
class Brand(models.Model):
    brand_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='brand_images/')

    def __str__(self):
        return self.name
    class Meta:
        db_table = "brand_table"


class Vehicle(models.Model):
    vehicle_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='vehicle_images/')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='vehicle_brand')

    def __str__(self):
        return self.name
    class Meta:
        db_table = "vehicle_table"


# Product related models
class Category(models.Model):
    category_id=models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='category_images/')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category_table"


class ModelYear(models.Model):
    modelyear_id=models.AutoField(primary_key=True)
    year = models.IntegerField()

    def __str__(self):
        return str(self.year)

    class Meta:
        db_table = "modelyear_table"

class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle_id= models.ForeignKey(Vehicle,on_delete=models.CASCADE, related_name='products')
    brand_id= models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    highlights = models.TextField()
    description = models.TextField()
    category_id= models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    modelyear_id= models.ForeignKey(ModelYear, on_delete=models.CASCADE, related_name='products',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "product_table"


class Cart(models.Model):
    cart_id=models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.product.title} ({self.quantity})'
    class Meta:
        db_table = "cart_table"


# Order Model
class Order(models.Model):
    order_id = models.CharField(max_length=20)
    cart_id= models.ForeignKey(Cart, on_delete=models.CASCADE)
    address_id= models.ForeignKey(Address, on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    delivery_charges = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

    class Meta:
        db_table = "order_table"
