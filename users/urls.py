from django.urls import path

urlpatterns = [
    path('', views.index, name='users-index')
]