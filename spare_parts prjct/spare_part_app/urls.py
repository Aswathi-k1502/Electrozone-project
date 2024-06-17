 from django.urls import path
from .views import *
urlpatterns = [
    path('brands/', brand_list_create, name='brand-list-create'),
    path('vehicles/', vehicle_list_create, name='vehicle-list-create'),
    path('categories/', category_list_create, name='category-list-create'),
    path('products/', product_list_create, name='product-list-create'),
    path('products/<int:pk>/', product_detail, name='product-detail'),

]
