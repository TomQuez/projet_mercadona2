from django.test import TestCase
import datetime
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from .models import Product,Promotion,Categorie,validate_inferior_100
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import SimpleUploadedFile
# Create your tests here.

class ObjectCreationTests(TestCase):
    def test_create_valid_product(self):
        #creation of a valid product
        product=Product(label="valid product",price=50.0,description="Description",category=None)
        product.save()
        #verification that the valid product exists in the database
        self.assertEqual(Product.objects.count(),1)
        
    def test_create_valid_promotion(self):
        #creation of a valid product
        product=Product(label="promotion product",price=100.0,description="Description",category=None)
        product.save()
        #creation of a promotion for the valid product
        promotion=Promotion(product=product,start_date="2023-01-01",end_date="2023-01-31",discount_percentage=10)
        promotion.save()
        #verification that the promotion exists in the database
        self.assertEqual(Promotion.objects.count(),1)
        
    def test_create_valid_categorie(self):
        #create a valid category
        categorie=Categorie(name="valid category")
        categorie.save()
        #verification that the category exists
        self.assertEqual(Categorie.objects.count(),1)
    
class PromotionModelTests(TestCase):
    def test_change_status_with_future_promotion(self):
        """change_status return False for future promotions"""
        future_day=datetime.date.today()+datetime.timedelta(days=45)
        future_promotion=Promotion(start_date=future_day)
        self.assertIs(future_promotion.change_status(),False)
    def test_change_status_with_past_promotion(self):
        """change_status return False for past promotion"""
        past_day=datetime.date.today()-datetime.timedelta(days=30)
        past_promotion=Promotion(end_date=past_day)
        self.assertIs(past_promotion.change_status(),False)
        
    def test_calculate_discounted_price(self):
        """calculate_discounted_price calculate the new price of a product if a promotion has a status True"""
        #creation of an example product for the test
        product=Product(label="example product",price=100.0)
        product.save()
        #creation of a promotion for this example p roduct
        today=datetime.date.today()
        start_date=today-datetime.timedelta(days=1)
        end_date=today+datetime.timedelta(days=1)
        promotion=Promotion(product=product,start_date=start_date,end_date=end_date,discount_percentage=20)
        promotion.save()
        #call method calculate_discounted_price
        discounted_price=promotion.calculate_discounted_price()
        #verification of the new discounted price
        self.assertEqual(discounted_price,80.0)
        
        
class ValidationTests(TestCase):
    def test_validate_inferior_100_valid_value(self):
        """validate_inferior_100 raise an error if the value is superior or equal to 100 or inferior or equal to zero"""
        value=50
        try:
            validate_inferior_100(value)
        except ValidationError:
            self.fail(f'validate_inferior_100 a échoué pour une valeur valide : {value}')
    
    def test_validate_inferior_100_invalid_value(self):
        """validate_inferior_100 raise an error if the value is superior or equal to 100 or inferior or equal to zero"""
        value=100
        with self.assertRaises(ValidationError):
            validate_inferior_100(value)
            
    def test_validate_inferior_100_invalid_negative_value(self):
        """validate_inferior_100 raise an error if the value is superior or equal to 100 or inferior or equal to zero"""
        value=-10
        with self.assertRaises(ValidationError):
            validate_inferior_100(value)
            
class ProductValidationTests(TestCase):
    def test_create_product_with_missing_label(self):
        #try to create a product without a label
        product = Product(price=50.0,description="Description", category=None)
       
        with self.assertRaises(ValidationError):
           
            product.full_clean()
    def test_create_product_with_missing_price(self):
        #try to create a product without a price
        product = Product(label="example without price",description="Description", category=None)
       
        with self.assertRaises(ValidationError):
           
            product.full_clean()
    def test_create_product_with_missing_description(self):
        #try to create a product without a description
        product = Product(label="example without description",price=50.0, category=None)
       
        with self.assertRaises(ValidationError):
           
            product.full_clean()
            
    def test_create_product_with_missing_category(self):
        #try to create a product without a category
        product = Product(label="example without category",price=50.0,description="description")
       
        with self.assertRaises(ValidationError):
           
            product.full_clean()
            
class CatalogViewsTests(TestCase):
    #create data for the tests
    def setUp(self):
        self.product=Product.objects.create(label="Product1",price=50.0,description="description")
        self.categorie=Categorie.objects.create(name="categorie1")
        self.promotion=Promotion.objects.create(product=self.product,start_date="2023-01-01",end_date="2023-01-31",discount_percentage=10)
        image_content=ContentFile(b'')
        image=SimpleUploadedFile("test_image.jpg",image_content.read(),content_type="image/jpeg")
        self.product.image=image
        self.product.save()
        
    def test_get_catalog_data(self):
        #test view get_catalog_data
        url=reverse('get_catalog_data')
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
        
    def test_index2(self):
        #test view index2
        url = reverse('index2')
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
        
class TemplateTests(TestCase):
    def test_index2_template(self):
        url = reverse('index2')
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
        
        self.assertContains(response,'Catalogue Mercadona')
        self.assertContains(response,'Bienvenue sur le catalogue de Mercadona')