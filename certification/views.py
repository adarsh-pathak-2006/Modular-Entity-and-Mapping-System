from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from drf_spectacular.utils import extend_schema
from .models import Certification
from .serializers import CertificationSerializer

@extend_schema(tags=['Certification'])
class CertificationListCreateAPIView(APIView):
    @extend_schema(summary="List all certifications", responses={200: CertificationSerializer(many=True)})
    def get(self, request):
        certifications = Certification.objects.all()
        serializer = CertificationSerializer(certifications, many=True)
        return Response(serializer.data)

    @extend_schema(summary="Create a certification", request=CertificationSerializer, responses={201: CertificationSerializer})
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Certification'])
class CertificationDetailAPIView(APIView):
    def get_object(self, pk):
        try: return Certification.objects.get(pk=pk)
        except Certification.DoesNotExist: raise Http404

    @extend_schema(summary="Retrieve a certification", responses={200: CertificationSerializer})
    def get(self, request, pk):
        certification = self.get_object(pk)
        serializer = CertificationSerializer(certification)
        return Response(serializer.data)

    @extend_schema(summary="Update a certification", request=CertificationSerializer, responses={200: CertificationSerializer})
    def put(self, request, pk):
        certification = self.get_object(pk)
        serializer = CertificationSerializer(certification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Partial update a certification", request=CertificationSerializer, responses={200: CertificationSerializer})
    def patch(self, request, pk):
        certification = self.get_object(pk)
        serializer = CertificationSerializer(certification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Delete a certification", responses={204: None})
    def delete(self, request, pk):
        certification = self.get_object(pk)
        certification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)