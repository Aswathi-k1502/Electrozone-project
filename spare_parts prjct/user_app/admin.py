from django.contrib import admin
from user_app.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Order)