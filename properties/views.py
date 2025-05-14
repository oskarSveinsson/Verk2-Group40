from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
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
    return render(request, 'properties/property_detail.html', {'property': prop})

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


@login_required
def start_finalize(request, offer_id):
    offer = get_object_or_404(PurchaseOffer, id=offer_id, buyer=request.user, status='Accepted')
    request.session['finalize_offer_id'] = offer_id
    return redirect('finalize', step='contact')

@login_required
def finalize(request, step):
    valid_steps = {
        'contact': 'contact',
        'payment_choice': 'payment_choice',
        'creditcard': 'CreditCard',
        'banktransfer': 'BankTransfer',
        'mortgage': 'Mortgage',
        'review': 'review',
    }
    step = valid_steps.get(step.lower())
    if not step:
        return redirect('/')
    offer_id = request.GET.get('offer_id') or request.session.get('finalize_offer_id')
    if not offer_id:
        return redirect('/')
    request.session['finalize_offer_id'] = offer_id

    offer = get_object_or_404(PurchaseOffer, id=offer_id, buyer=request.user, status='Accepted')

    if step == 'contact':
        print("🔍 FINALIZE STEP: contact step hit")
        print("🔍 Attempting get_or_create for FinalizedOffer...")
        try:
            finalized_offer, created = FinalizedOffer.objects.get_or_create(offer=offer)
            print(f"FinalizedOffer for offer_id {offer_id} created={created}")
            contact = ContactInfo.objects.get(offer=offer)
            init = {
                'street': contact.street,
                'city': contact.city,
                'postal_code': contact.postal_code,
                'country': contact.country,
                'national_id': contact.national_id,
            }
        except ContactInfo.DoesNotExist:
            init = {}
        form = ContactForm(request.POST or None, initial=init)
        if request.method == 'POST' and form.is_valid():
            data = form.cleaned_data
            ContactInfo.objects.update_or_create(
                offer=offer,
                defaults={
                    'street': data['street'],
                    'city': data['city'],
                    'postal_code': data['postal_code'],
                    'country': data['country'],
                    'national_id': data['national_id'],
                }
            )
            return redirect('finalize', step='payment_choice')
        return render(request, 'properties/finalize_contact.html', {'form': form, 'offer': offer})

    elif step == 'payment_choice':
        try:
            payment = PaymentInfo.objects.get(offer=offer)
            init = {'payment_method': payment.pay_method,}
        except PaymentInfo.DoesNotExist:
            init = {}
        form = PaymentChoiceForm(request.POST or None, initial=init)
        if request.method == 'POST' and form.is_valid():
            method = form.cleaned_data['payment_method']
            request.session['payment_method'] = method

            step_key = None
            for key, value in valid_steps.items():
                if value == method:
                    step_key = key
                    break

            return redirect('finalize', step=step_key)

        return render(request, 'properties/finalize_payment_choice.html', {'form': form, 'offer': offer})

    elif step in ['CreditCard', 'BankTransfer', 'Mortgage']:
        method = step
        payment_defaults = {}
        try:
            payment = PaymentInfo.objects.get(offer=offer)
            if method == 'CreditCard':
                payment_defaults = {
                    'card_holder': payment.card_holder,
                    'card_number': payment.card_number,
                    'expiration_date': payment.expiration_date,
                    'cvc': payment.cvc,
                }
            elif method == 'BankTransfer':
                payment_defaults = {
                    'account_number': payment.account_number,
                }
            elif method == 'Mortgage':
                payment_defaults = {
                    'mortgage_provider': payment.mortgage_provider,
                }
        except PaymentInfo.DoesNotExist:
            pass

        form_class = {
            'CreditCard': CreditCardForm,
            'BankTransfer': BankTransferForm,
            'Mortgage': MortgageForm
        }[method]

        form = form_class(request.POST or None, initial=payment_defaults)
        if request.method == 'POST' and form.is_valid():
            data = form.cleaned_data
            defaults = {'pay_method': method}
            if method == 'CreditCard':
                defaults.update({
                    'card_holder': data['card_holder'],
                    'card_number': data['card_number'],
                    'expiration_date': data['expiration_date'],
                    'cvc': data['cvc'],
                })
            elif method == 'BankTransfer':
                defaults.update({
                    'account_number': data['account_number'],
                })
            elif method == 'Mortgage':
                defaults.update({
                    'mortgage_provider': data['mortgage_provider'],
                })
            PaymentInfo.objects.update_or_create(offer=offer, defaults=defaults)
            return redirect('finalize', step='review')
        return render(request, f"properties/finalize_{method}.html", {'form': form, 'offer': offer})

    elif step == 'review':
        contact = ContactInfo.objects.get(offer=offer)
        payment = PaymentInfo.objects.get(offer=offer)
        return render(request, 'properties/finalize_review.html', {'offer': offer, 'contact': contact, 'payment': payment})

    else:
        return redirect('/')

@login_required
def confirm_finalize(request):
    offer_id = request.session.get('finalize_offer_id')
    if not offer_id:
        return redirect('/')
    offer = get_object_or_404(PurchaseOffer, id=offer_id, buyer=request.user, status='Accepted')
    FinalizedOffer.objects.get_or_create(offer=offer)
    return render(request, 'properties/finalize_complete.html', {'offer': offer})

