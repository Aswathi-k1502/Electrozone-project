from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Vehicle)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(ModelYear)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)