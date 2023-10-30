from django.shortcuts import render
from mercadona_app.models import Product,Promotion,Categorie
from django.views import generic
from mercadona_app.forms import FiltreCategorieForm 


# Create your views here.
def index(request):
    product_list=Product.objects.all()
    promotion_list=Promotion.objects.all()
    category_list=Categorie.objects.all()
    

    
    context={
        'product_list':product_list,
        'promotion_list':promotion_list,
        'category_list':category_list,
    }
    

    
    
    
    return render(request,'index.html',context=context)


def product_list(request):
    
    categories=Categorie.objects.all()
    selected_category=request.GET.get('category',None)
    if selected_category:
        products=Product.objects.filter(category__name=selected_category)
    else:
        products=Product.objects.all()

        
    context={
        'categories':categories,
        'selected_category':selected_category,
        'products':products,
    }
    return render(request,'categories.html',context=context)