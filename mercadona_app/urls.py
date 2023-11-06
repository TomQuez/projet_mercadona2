from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('get_catalog_data/',views.get_catalog_data,name='get_catalog_data'),
    path('index2',views.index2,name="index2")
]