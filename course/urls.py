from django.urls import path
from .views import CourseListCreateAPIView, CourseDetailAPIView

urlpatterns = [
    path('', CourseListCreateAPIView.as_view(), name='course-list-create'),
    path('<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
]