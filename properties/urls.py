from django.urls import path
from . import views
urlpatterns = [
    path('', views.get_properties, name='properties-index'),
    path('<int:id>', views.get_property_detail, name='property-detail'),
    path('<int:property_id>/submit_offer', views.submit_offer, name='submit-offer'),
    path('<int:property_id>/offer_success', views.offer_success, name='offer-success'),
]