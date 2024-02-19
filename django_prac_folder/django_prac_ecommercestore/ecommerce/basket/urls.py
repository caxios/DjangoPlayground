from . import views
from django.urls import path

# Define the application namespace for URL names defined within store/urls.py.
app_name='basket'

urlpatterns = [
    path('', views.basket_summary, name='basket_summary'),
    path('add/', views.basket_add, name='basket_add'),

]