from django.urls import path
from . import views
urlpatterns=[
    # path('',views.index,name='index'),
    path('',views.ProductListView.as_view(),name='products')
]