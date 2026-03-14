from rest_framework import serializers
from .models import VendorProductMapping
from vendor.models import Vendor
from product.models import Product

class VendorProductMappingSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = VendorProductMapping
        fields = ['id', 'vendor', 'product', 'primary_mapping', 'is_active', 'created_at', 'updated_at', 'vendor_name', 'product_name']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # Get the vendor instance (passed from view context or from instance if updating)
        vendor = data.get('vendor')
        
        # If this is an update (instance exists), handle vendor retrieval differently
        if self.instance:
            # If vendor is not in data, use existing vendor
            vendor = data.get('vendor', self.instance.vendor)
            
        # Check if this is being set as primary
        is_primary = data.get('primary_mapping', False)
        
        if is_primary:
            # Check if another primary mapping already exists for this vendor
            existing_primary = VendorProductMapping.objects.filter(
                vendor=vendor, 
                primary_mapping=True
            )
            
            # If updating, exclude the current instance from the check
            if self.instance:
                existing_primary = existing_primary.exclude(pk=self.instance.pk)
                
            if existing_primary.exists():
                raise serializers.ValidationError(
                    {"primary_mapping": "A primary mapping already exists for this vendor. Only one primary mapping is allowed."}
                )
        
        return data