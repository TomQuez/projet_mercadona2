from django.db import models
from django.urls import reverse
import uuid
import datetime
import math
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_inferior_100(value):
    if value>=100:
        raise ValidationError(_("%(value)s is not inferior to 100"),params={"value":value})

# Create your models here.
class Categorie (models.Model):
    """This object represent a category for a product."""
    name=models.CharField(max_length=100,help_text="Enter a name for the category(e.g. sport)")
    
    def __str__(self):
        """this function return a string to identify the instance of the object's class """
        return self.name
    
class Product(models.Model):
    """This object represent a product"""
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text="Unique ID for this particular product")
    label=models.CharField(max_length=200,help_text="Enter a label for the product")
    price=models.DecimalField(max_digits=10,decimal_places=2, help_text="Enter a price for the product")
    description=models.TextField(max_length=1000,help_text="Enter a brief description of the product")
    image=models.ImageField(upload_to="images/")
    category=models.ForeignKey(Categorie,on_delete=models.SET_NULL,null=True, help_text="select a category for the product")
    
    class Meta :
        ordering=['label']
    
    def __str__(self):
        """Function used to manipulate the objects Product in the database"""
        return self.label
    
    def get_absolute_url(self):
        """This function is used to display the content of an object Product"""
        return reverse('product-detail',args=[str(self.id)])
    
    def get_price(self):
        """return the price of the product"""
        
        return self.price
    
    
class Promotion(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text="Unique ID for this promotion")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    start_date=models.DateField()
    end_date=models.DateField()
    discount_percentage=models.PositiveIntegerField(validators=[validate_inferior_100],help_text="Enter a percentage for the promotion. it must be positive and under 100")
    
    
    
    def __str__(self):
        """Function used to manipulate a promotion in the database"""
        result_discount=str(self.discount_percentage)
        return f'{self.product} : promotion de {result_discount} %'
    
    def change_status(self):
        if self.start_date <= datetime.date.today() and self.end_date>=datetime.date.today():
            self.status=True
            return self.status
    
    def calculate_discounted_price(self):
        if datetime.date.today()>=self.start_date and datetime.date.today()<=self.end_date: 
            self.product.price= self.product.price-(self.product.price*self.discount_percentage/100)
            return self.product.price
        