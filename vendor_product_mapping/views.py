from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from drf_spectacular.utils import extend_schema
from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer

@extend_schema(tags=['Vendor Product Mapping'])
class VendorProductMappingListCreateAPIView(APIView):
    @extend_schema(
        summary="List all vendor-product mappings",
        responses={200: VendorProductMappingSerializer(many=True)}
    )
    def get(self, request):
        # Support filtering: /api/vendor-product-mappings/?vendor_id=1
        vendor_id = request.query_params.get('vendor_id')
        product_id = request.query_params.get('product_id')
        
        mappings = VendorProductMapping.objects.all()
        
        if vendor_id:
            mappings = mappings.filter(vendor_id=vendor_id)
        if product_id:
            mappings = mappings.filter(product_id=product_id)
            
        serializer = VendorProductMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create a vendor-product mapping",
        request=VendorProductMappingSerializer,
        responses={201: VendorProductMappingSerializer}
    )
    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Vendor Product Mapping'])
class VendorProductMappingDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return VendorProductMapping.objects.get(pk=pk)
        except VendorProductMapping.DoesNotExist:
            raise Http404

    @extend_schema(
        summary="Retrieve a specific mapping",
        responses={200: VendorProductMappingSerializer}
    )
    def get(self, request, pk):
        mapping = self.get_object(pk)
        serializer = VendorProductMappingSerializer(mapping)
        return Response(serializer.data)

    @extend_schema(
        summary="Update a mapping",
        request=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer}
    )
    def put(self, request, pk):
        mapping = self.get_object(pk)
        serializer = VendorProductMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Partial update a mapping",
        request=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer}
    )
    def patch(self, request, pk):
        mapping = self.get_object(pk)
        serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete a mapping",
        responses={204: None}
    )
    def delete(self, request, pk):
        mapping = self.get_object(pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)