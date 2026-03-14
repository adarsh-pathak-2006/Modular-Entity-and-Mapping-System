from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from drf_spectacular.utils import extend_schema
from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer

@extend_schema(tags=['Product Course Mapping'])
class ProductCourseMappingListCreateAPIView(APIView):
    @extend_schema(summary="List mappings", responses={200: ProductCourseMappingSerializer(many=True)})
    def get(self, request):
        product_id = request.query_params.get('product_id')
        mappings = ProductCourseMapping.objects.all()
        if product_id:
            mappings = mappings.filter(product_id=product_id)
        serializer = ProductCourseMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    @extend_schema(summary="Create mapping", request=ProductCourseMappingSerializer, responses={201: ProductCourseMappingSerializer})
    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Product Course Mapping'])
class ProductCourseMappingDetailAPIView(APIView):
    def get_object(self, pk):
        try: return ProductCourseMapping.objects.get(pk=pk)
        except ProductCourseMapping.DoesNotExist: raise Http404

    @extend_schema(summary="Retrieve mapping", responses={200: ProductCourseMappingSerializer})
    def get(self, request, pk):
        mapping = self.get_object(pk)
        serializer = ProductCourseMappingSerializer(mapping)
        return Response(serializer.data)

    @extend_schema(summary="Update mapping", request=ProductCourseMappingSerializer, responses={200: ProductCourseMappingSerializer})
    def put(self, request, pk):
        mapping = self.get_object(pk)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Partial update mapping", request=ProductCourseMappingSerializer, responses={200: ProductCourseMappingSerializer})
    def patch(self, request, pk):
        mapping = self.get_object(pk)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Delete mapping", responses={204: None})
    def delete(self, request, pk):
        mapping = self.get_object(pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)