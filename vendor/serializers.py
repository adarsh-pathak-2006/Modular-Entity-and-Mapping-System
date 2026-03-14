from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'code', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    # Validation: Ensure code is unique
    def validate_code(self, value):
        # If updating, exclude current instance
        if self.instance:
            if Vendor.objects.filter(code=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("A vendor with this code already exists.")
        else:
            if Vendor.objects.filter(code=value).exists():
                raise serializers.ValidationError("A vendor with this code already exists.")
        return value