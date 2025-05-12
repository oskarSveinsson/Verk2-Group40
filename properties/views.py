from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, PurchaseOffer
from .forms import PurchaseOfferForm
from django.contrib.auth.decorators import login_required

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

    user_offer = None
    if request.user.is_authenticated:
        user_offer = PurchaseOffer.objects.filter(buyer=request.user, property=prop).first()

    return render(request, 'properties/property_detail.html', {
        'property': prop,
        'user_offer': user_offer
    })

@login_required
def submit_offer(request, property_id):
    prop = get_object_or_404(Property, pk=property_id)

    if request.method == 'POST':
        form = PurchaseOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.property = prop
            offer.buyer = request.user
            offer.status = 'Pending'
            offer.save()
            return redirect('offer_success', property_id=prop.id)
    else:
        form = PurchaseOfferForm()

    return render(request, 'properties/submit_offer.html', {'form': form, 'property': prop})

def offer_success(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    return render(request, 'properties/offer_success.html', {'property': property})

