from rest_framework import serializers
from .models import ProductCourseMapping

class ProductCourseMappingSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = ProductCourseMapping
        fields = ['id', 'product', 'course', 'primary_mapping', 'is_active', 'created_at', 'updated_at', 'product_name', 'course_name']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        product = data.get('product')
        if self.instance:
            product = data.get('product', self.instance.product)
            
        is_primary = data.get('primary_mapping', False)
        
        if is_primary:
            existing_primary = ProductCourseMapping.objects.filter(product=product, primary_mapping=True)
            if self.instance:
                existing_primary = existing_primary.exclude(pk=self.instance.pk)
            if existing_primary.exists():
                raise serializers.ValidationError({"primary_mapping": "A primary mapping already exists for this product."})
        return data