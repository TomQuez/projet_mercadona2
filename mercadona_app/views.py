from django.shortcuts import render
from mercadona_app.models import Product,Promotion,Categorie
from django.views import generic
from django.core.paginator import Paginator



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


