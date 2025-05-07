from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='properties-index'),
    path('<int:id>', views.get_properties_by_id, name='properties-by-id'),
]