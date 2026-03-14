from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from drf_spectacular.utils import extend_schema
from .models import Vendor
from .serializers import VendorSerializer

@extend_schema(tags=['Vendor'])
class VendorListCreateAPIView(APIView):
    @extend_schema(
        summary="List all vendors",
        responses={200: VendorSerializer(many=True)}
    )
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create a vendor",
        request=VendorSerializer,
        responses={201: VendorSerializer}
    )
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Vendor'])
class VendorDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            raise Http404

    @extend_schema(
        summary="Retrieve a vendor",
        responses={200: VendorSerializer}
    )
    def get(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    @extend_schema(
        summary="Update a vendor",
        request=VendorSerializer,
        responses={200: VendorSerializer}
    )
    def put(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Partial update a vendor",
        request=VendorSerializer,
        responses={200: VendorSerializer}
    )
    def patch(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete a vendor",
        responses={204: None}
    )
    def delete(self, request, pk):
        vendor = self.get_object(pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)