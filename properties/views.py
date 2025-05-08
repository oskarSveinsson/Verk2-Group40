from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Property

def index(request):
    return HttpResponse(f"Response from {request.path}")

def get_properties_by_id(request, id):
    return HttpResponse(f"Response from {request.path} with id {id}")

def get_properties(request):
    props = Property.objects.prefetch_related('images').all()
    return render(request, 'properties/properties.html', {'properties': props})

def get_property_detail(request, id):
    prop = get_object_or_404(Property, id=id)
    return render(request, 'properties/property_detail.html', {'property': prop})

