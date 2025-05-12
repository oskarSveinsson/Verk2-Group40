from django.urls import path
from . import views
urlpatterns = [
    path('', views.get_properties, name='properties-index'),
    path('<int:id>', views.get_property_detail, name='property-detail'),
    path('<int:property_id>/submit_offer', views.submit_offer, name='submit_offer'),
    path('<int:property_id>/offer_success', views.offer_success, name='offer_success'),
    path('finalize/<int:offer_id>', views.start_finalize, name='start_finalize' ),
    path('finalize/step/<str:step>', views.finalize, name='finalize'),
    path('finalize/confirm/', views.confirm_finalize, name='finalize_confirm'),
]