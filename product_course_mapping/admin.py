from django.contrib import admin
from .models import ProductCourseMapping

@admin.register(ProductCourseMapping)
class ProductCourseMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'course', 'primary_mapping', 'is_active')
    list_filter = ('primary_mapping', 'is_active', 'product', 'course')
    search_fields = ('product__name', 'course__name')
    raw_id_fields = ('product', 'course')