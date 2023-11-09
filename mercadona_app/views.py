from django.shortcuts import render
from mercadona_app.models import Product,Promotion,Categorie
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.core import serializers
import datetime
from math import ceil
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def index(request):
    
    promotion_list=Promotion.objects.all()
   
    categories=Categorie.objects.all()
    selected_category=request.GET.get('category',None)
    if selected_category:
        product_list=Product.objects.filter(category__name=selected_category)
    else:
        product_list=Product.objects.all()
        
    paginator=Paginator(product_list,3)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    
    context={
        'product_list':page_obj,
        'promotion_list':promotion_list,
        'categories':categories,
        'selected_category':selected_category
    }
    

    
    
    
    return render(request,'index.html',context=context)



def get_catalog_data(request):
    products=Product.objects.all()
    promotions=Promotion.objects.all()
    categories=Categorie.objects.all()
    catalogue_data=[]
  
    
    category_id=request.GET.get('category')
    if category_id is not None and category_id!='':
        products=Product.objects.filter(category=category_id)
    
    
    for product in products:
        product_data={
            'id':str(product.id),
            'label':product.label,
            'price':str(product.price),
            'description':product.description,
            'image':product.image.url,
            'category':product.category.name if product.category else '',
            'categoryId':product.category.id if product.category else '',
            'promotion':None,
        }
        for promotion in promotions:
            if promotion.product==product:
                product_data['promotion']={
                    'start_date':promotion.start_date,
                    'end_date':promotion.end_date,
                    'discount_percentage':promotion.discount_percentage,
                    'status':promotion.status
                    
                }
                if promotion.start_date<=datetime.date.today()<=promotion.end_date:
                    discounted_price=product.price-(product.price*promotion.discount_percentage/100)
                    product_data['price']=str(discounted_price)
                    product_data['promotion']['status']=True
        catalogue_data.append(product_data)
        
    context={
        'products':catalogue_data,     
        'categories':list(categories.values()),}
    return JsonResponse(context) 

def index2(request):
    return render(request,'index2.html')