from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'code', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_code(self, value):
        if self.instance:
            if Product.objects.filter(code=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("A product with this code already exists.")
        else:
            if Product.objects.filter(code=value).exists():
                raise serializers.ValidationError("A product with this code already exists.")
        return value