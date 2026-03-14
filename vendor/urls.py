from django.urls import path
from .views import VendorListCreateAPIView, VendorDetailAPIView

urlpatterns = [
    path('', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('<int:pk>/', VendorDetailAPIView.as_view(), name='vendor-detail'),
]