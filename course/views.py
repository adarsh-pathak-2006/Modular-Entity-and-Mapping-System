from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from drf_spectacular.utils import extend_schema
from .models import Course
from .serializers import CourseSerializer

@extend_schema(tags=['Course'])
class CourseListCreateAPIView(APIView):
    @extend_schema(summary="List all courses", responses={200: CourseSerializer(many=True)})
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    @extend_schema(summary="Create a course", request=CourseSerializer, responses={201: CourseSerializer})
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Course'])
class CourseDetailAPIView(APIView):
    def get_object(self, pk):
        try: return Course.objects.get(pk=pk)
        except Course.DoesNotExist: raise Http404

    @extend_schema(summary="Retrieve a course", responses={200: CourseSerializer})
    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    @extend_schema(summary="Update a course", request=CourseSerializer, responses={200: CourseSerializer})
    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Partial update a course", request=CourseSerializer, responses={200: CourseSerializer})
    def patch(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Delete a course", responses={204: None})
    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)