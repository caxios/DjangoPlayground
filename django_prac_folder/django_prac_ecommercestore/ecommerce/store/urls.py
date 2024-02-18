from . import views
from django.urls import path

# define the application namespace for URL names defined within store/urls.py.
app_name='store'

urlpatterns = [
    path('', views.product_all, name='product_all'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/<slug:category_slug>/', views.category_list, name='category_list'),
]