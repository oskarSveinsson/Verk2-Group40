from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from users.forms.profile_form import ProfileUpdateForm, ProfileImageForm
from users.models import UserProfile
from properties.models import Property, PurchaseOffer


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # or your homepage
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=user)
        image_form = ProfileImageForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and image_form.is_valid():
            user_form.save()
            image_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = ProfileUpdateForm(instance=user)
        image_form = ProfileImageForm(instance=profile)

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'image_form': image_form,
        'profile': profile
    })

@login_required
def purchase_offers(request):
    offers = PurchaseOffer.objects.select_related('property__seller').filter(buyer=request.user)
    return render(request, 'users/my_offers.html', {'offers': offers})

@login_required
def seller_dash(request):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('/')

    properties = Property.objects.filter(seller=request.user)

    offers = PurchaseOffer.objects.filter(property__in=properties)

    return render(request, 'seller_dash.html', {'offers': offers})

@login_required
def accept_offer(request, offer_id):
    offer = get_object_or_404(PurchaseOffer, id=offer_id, property__seller=request.user)
    offer.status = 'Accepted'
    offer.save()
    offer.property.update_status()
    return redirect('seller_dash')

@login_required
def decline_offer(request, offer_id):
    offer = get_object_or_404(PurchaseOffer, id=offer_id, property__seller=request.user)
    offer.status = 'Declined'
    offer.save()
    return redirect('seller_dash')

