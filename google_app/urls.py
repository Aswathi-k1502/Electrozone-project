from django.urls import path
from .views import UserDetail

urlpatterns = [
    path('user/', UserDetail.as_view(), name='user-detail'),
]
