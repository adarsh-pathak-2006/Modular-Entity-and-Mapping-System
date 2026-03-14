from rest_framework import serializers
from .models import CourseCertificationMapping

class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    certification_name = serializers.CharField(source='certification.name', read_only=True)

    class Meta:
        model = CourseCertificationMapping
        fields = ['id', 'course', 'certification', 'primary_mapping', 'is_active', 'created_at', 'updated_at', 'course_name', 'certification_name']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        course = data.get('course')
        if self.instance:
            course = data.get('course', self.instance.course)
            
        is_primary = data.get('primary_mapping', False)
        
        if is_primary:
            existing_primary = CourseCertificationMapping.objects.filter(course=course, primary_mapping=True)
            if self.instance:
                existing_primary = existing_primary.exclude(pk=self.instance.pk)
            if existing_primary.exists():
                raise serializers.ValidationError({"primary_mapping": "A primary mapping already exists for this course."})
        return data