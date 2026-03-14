from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from drf_spectacular.utils import extend_schema
from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer

@extend_schema(tags=['Course Certification Mapping'])
class CourseCertificationMappingListCreateAPIView(APIView):
    @extend_schema(summary="List mappings", responses={200: CourseCertificationMappingSerializer(many=True)})
    def get(self, request):
        course_id = request.query_params.get('course_id')
        mappings = CourseCertificationMapping.objects.all()
        if course_id:
            mappings = mappings.filter(course_id=course_id)
        serializer = CourseCertificationMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    @extend_schema(summary="Create mapping", request=CourseCertificationMappingSerializer, responses={201: CourseCertificationMappingSerializer})
    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Course Certification Mapping'])
class CourseCertificationMappingDetailAPIView(APIView):
    def get_object(self, pk):
        try: return CourseCertificationMapping.objects.get(pk=pk)
        except CourseCertificationMapping.DoesNotExist: raise Http404

    @extend_schema(summary="Retrieve mapping", responses={200: CourseCertificationMappingSerializer})
    def get(self, request, pk):
        mapping = self.get_object(pk)
        serializer = CourseCertificationMappingSerializer(mapping)
        return Response(serializer.data)

    @extend_schema(summary="Update mapping", request=CourseCertificationMappingSerializer, responses={200: CourseCertificationMappingSerializer})
    def put(self, request, pk):
        mapping = self.get_object(pk)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Partial update mapping", request=CourseCertificationMappingSerializer, responses={200: CourseCertificationMappingSerializer})
    def patch(self, request, pk):
        mapping = self.get_object(pk)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Delete mapping", responses={204: None})
    def delete(self, request, pk):
        mapping = self.get_object(pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)