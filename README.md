Django Modular Entity & Mapping System
This project is a Django REST Framework backend built for an intern assignment. It manages master entities (Vendor, Product, Course, Certification) and their mappings using pure APIView classes.

Features
Modular app structure (7 separate apps).
CRUD APIs for all entities.
Custom Validations (Duplicate prevention, Single primary mapping per parent).
API Documentation using Swagger (drf-spectacular).
Query-param based filtering for mappings.
Tech Stack
Python 3.10
Django 5.2
Django REST Framework
drf-spectacular (for Swagger/OpenAPI)
Setup Instructions
1. Clone the Repository
git clone <your-repo-url>cd core
2. Create Virtual Environment & Install Dependencies
bash

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install django djangorestframework drf-spectacular
3. Apply Migrations
bash

python manage.py makemigrations
python manage.py migrate
4. Run the Server
bash

python manage.py runserver
5. Access API Documentation
Open your browser and go to:

Swagger UI: http://127.0.0.1:8000/swagger/
ReDoc: http://127.0.0.1:8000/redoc/
API Endpoints
Master Entities
Entity
List/Create
Detail (R/U/D)
Vendor	/api/vendors/	/api/vendors/{id}/
Product	/api/products/	/api/products/{id}/
Course	/api/courses/	/api/courses/{id}/
Certification	/api/certifications/	/api/certifications/{id}/

Mapping Entities
Mapping
List/Create
Detail (R/U/D)
Vendor-Product	/api/vendor-product-mappings/	/api/vendor-product-mappings/{id}/
Product-Course	/api/product-course-mappings/	/api/product-course-mappings/{id}/
Course-Certification	/api/course-certification-mappings/	/api/course-certification-mappings/{id}/

Filtering Examples
Get products for a specific vendor: /api/vendor-product-mappings/?vendor_id=1
Get courses for a specific product: /api/product-course-mappings/?product_id=1
Validation Rules Implemented
Unique Code: Master entities require unique code fields.
Duplicate Mapping: Prevents the same pair (e.g., Vendor A + Product B) from being mapped twice.
Primary Mapping: Only one mapping per parent can be marked primary_mapping=True. Attempting to add a second primary mapping returns a validation error.

python manage.py seed_data


---

#### 2. The Seed Script (Sample Data)
This fulfills the "Sample Data" requirement. We will create a custom management command.

**Step A:** Create the folder structure inside your `core` app:
`core/management/commands/seed_data.py`
*(You might need to create the `management` and `commands` folders manually).*

**Step B:** Put this code in `core/management/commands/seed_data.py`:

```python
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
