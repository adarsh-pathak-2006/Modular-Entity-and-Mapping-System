from django.urls import path
from .views import CourseCertificationMappingListCreateAPIView, CourseCertificationMappingDetailAPIView

urlpatterns = [
    path('', CourseCertificationMappingListCreateAPIView.as_view(), name='course-certification-mapping-list-create'),
    path('<int:pk>/', CourseCertificationMappingDetailAPIView.as_view(), name='course-certification-mapping-detail'),
]