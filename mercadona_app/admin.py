from django.contrib import admin

from mercadona_app.models import Product,Promotion,Categorie
# Register your models here.
admin.site.register(Product)
admin.site.register(Promotion)
admin.site.register(Categorie)