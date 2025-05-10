from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Property

def index(request):
    return HttpResponse(f"Response from {request.path}")

def get_properties_by_id(request, id):
    return HttpResponse(f"Response from {request.path} with id {id}")

def get_properties(request):
    props = Property.objects.prefetch_related('images').all()

    postal_code = request.GET.get('postal_code')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    property_type = request.GET.get('property_type')
    search = request.GET.get('search')
    order_by = request.GET.get('order_by')

    if postal_code:
        props = props.filter(postal_code=postal_code)

    if price_min:
        props = props.filter(listing_price__gte=price_min)

    if price_max:
        props = props.filter(listing_price__lte=price_max)

    if property_type:
        props = props.filter(property_type__iexact=property_type)

    if search:
        props = props.filter(street__icontains=search)

    if order_by in ['listing_price', 'street']:
        props = props.order_by(order_by)

    return render(request, 'properties/properties.html', {'properties': props})

def get_property_detail(request, id):
    prop = get_object_or_404(Property, id=id)
    return render(request, 'properties/property_detail.html', {'property': prop})

