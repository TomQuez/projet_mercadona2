from django.contrib import admin

from mercadona_app.models import Product,Promotion,Categorie
# Register your models here.
#admin.site.register(Product)
# admin.site.register(Promotion)
# admin.site.register(Categorie)



@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display=('product','discount_percentage','start_date','end_date','calculate_discounted_price')
   
    list_filter=('start_date','end_date')

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    pass

class PromotionInline(admin.TabularInline):
    model=Promotion
    extra=0
    
class ProductAdmin(admin.ModelAdmin):
    list_display=('label','id','category','price')
    list_filter=('category','price')
    inlines=[PromotionInline]
    
    
admin.site.register(Product,ProductAdmin)