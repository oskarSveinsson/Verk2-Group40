from django.urls import path
from . import views
urlpatterns = [
    path('', views.get_properties, name='properties-index'),
    path('<int:id>', views.get_property_detail, name='property-detail'),
]