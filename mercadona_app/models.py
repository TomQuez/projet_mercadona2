from django.db import models
from django.urls import reverse
import uuid
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField


def validate_inferior_100(value):
    if value>=100 or value<=0 :
        raise ValidationError(_("%(value)s is not inferior to 100"),params={"value":value})
def validate_image_extension(value):
    if not value.name.endswith(('.jpg','.jpeg','.png','.gif')):
        raise ValidationError("Seuls les fichiers image .jpg, .jpeg, ,.gif et .png sont autorisés")

# Create your models here.
class Categorie (models.Model):
    """This object represent a category for a product."""
    name=models.CharField(max_length=100,help_text="Enter a name for the category(e.g. sport)")
    # history=AuditlogHistoryField()
    
    def __str__(self):
        """this function return a string to identify the instance of the object's class """
        return self.name
    
class Product(models.Model):
    """This object represent a product"""
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text="Unique ID for this particular product")
    label=models.CharField(max_length=200,help_text="Enter a label for the product",null=False)
    price=models.DecimalField(max_digits=10,decimal_places=2, help_text="Enter a price for the product",null=False)
    description=models.TextField(max_length=1000,help_text="Enter a brief description of the product",null=False)
    image=models.ImageField(upload_to="images/",validators=[validate_image_extension])
    category=models.ForeignKey(Categorie,on_delete=models.SET_NULL,null=True, help_text="select a category for the product")
    # history=AuditlogHistoryField()
 
    
    class Meta :
        ordering=['label']
    
    def __str__(self):
        """Function used to manipulate the objects Product in the database"""
        return self.label
    
    # def get_absolute_url(self):
    #     """This function is used to display the content of an object Product"""
    #     return reverse('product-detail',args=[str(self.id)])
    
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
    # history=AuditlogHistoryField()
    
    
    
    def __str__(self):
        """Function used to manipulate a promotion in the database"""
        result_discount=str(self.discount_percentage)
        return f'{self.product} : promotion de {result_discount} %'
    
    def change_status(self):
        if self.start_date is not None and self.end_date is not None:
        
            if self.start_date <= datetime.date.today() and self.end_date>=datetime.date.today():
                self.status=True
                return self.status
        else :
            self.status=False
            return self.status
    
    def calculate_discounted_price(self):
        
        if datetime.date.today()>=self.start_date and datetime.date.today()<=self.end_date: 
            self.product.price= self.product.price-(self.product.price*self.discount_percentage/100)
            return self.product.price
# auditlog.register(Product, Promotion, Categorie)