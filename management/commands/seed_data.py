from django.core.management.base import BaseCommand
from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        # Clear existing data to avoid duplicates
        VendorProductMapping.objects.all().delete()
        ProductCourseMapping.objects.all().delete()
        CourseCertificationMapping.objects.all().delete()
        Vendor.objects.all().delete()
        Product.objects.all().delete()
        Course.objects.all().delete()
        Certification.objects.all().delete()

        self.stdout.write("Creating Master Data...")

        # Create Master Entities
        v1 = Vendor.objects.create(name="TechCorp", code="V001", description="Tech Vendor")
        v2 = Vendor.objects.create(name="EduCorp", code="V002", description="Education Vendor")

        p1 = Product.objects.create(name="Python Pro", code="P001", description="Python Course Product")
        p2 = Product.objects.create(name="Django Master", code="P002", description="Django Course Product")

        c1 = Course.objects.create(name="Python 101", code="C101", description="Basic Python")
        c2 = Course.objects.create(name="Django 101", code="C102", description="Basic Django")

        cert1 = Certification.objects.create(name="Certified Pythonist", code="CERT1")
        cert2 = Certification.objects.create(name="Certified Django Dev", code="CERT2")

        self.stdout.write("Creating Mappings...")

        # Create Mappings
        # Vendor -> Product
        VendorProductMapping.objects.create(vendor=v1, product=p1, primary_mapping=True)
        VendorProductMapping.objects.create(vendor=v1, product=p2, primary_mapping=False)
        
        # Product -> Course
        ProductCourseMapping.objects.create(product=p1, course=c1, primary_mapping=True)
        ProductCourseMapping.objects.create(product=p2, course=c2, primary_mapping=True)

        # Course -> Certification
        CourseCertificationMapping.objects.create(course=c1, certification=cert1, primary_mapping=True)
        CourseCertificationMapping.objects.create(course=c2, certification=cert2, primary_mapping=True)

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
