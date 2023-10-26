from django.shortcuts import render
from mercadona_app.models import Product,Promotion,Categorie
from django.views import generic

# Create your views here.
def index(request):
    product_list=Product.objects.all()
    promotion_list=Promotion.objects.all()
    context={
        'product_list':product_list,
        'promotion_list':promotion_list,
    }
    

    
    
    
    return render(request,'index.html',context=context)
# class ProductListView(generic.ListView):
#     model=Product
    
    # context_object_name='my_product_list'
    # queryset=Product.objects.filter(label__icontains='t')[:4]
    # template_name='products/my_arbitrary_template_name_list.html'