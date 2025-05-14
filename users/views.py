from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from users.forms import ProfileUpdateForm, ProfileImageForm, UserRegisterForm
from users.models import UserProfile
from properties.models import PurchaseOffer, Property


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'seller_profile'):
                return redirect('seller_dash')
            return redirect('profile')
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

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Registration complete!")
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def seller_dash(request):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('/')

    seller = request.user.seller_profile

    properties = Property.objects.filter(seller=seller)

    offers = PurchaseOffer.objects.filter(property__in=properties)

    return render(request, 'users/seller_dash.html', {'offers': offers})

@login_required
def accept_offer(request, offer_id):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('/')

    seller = request.user.seller_profile
    offer = get_object_or_404(PurchaseOffer, id=offer_id, property__seller=seller)

    has_accepted = PurchaseOffer.objects.filter(property=offer.property, status='Accepted').exists()

    if has_accepted:
        messages.error(request, "This property already has an accepted offer")
        return redirect('seller_dash')
    offer.status = 'Accepted'
    offer.save()
    offer.property.update_status()
    return redirect('seller_dash')

@login_required
def decline_offer(request, offer_id):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('/')

    seller = request.user.seller_profile
    offer = get_object_or_404(PurchaseOffer, id=offer_id, property__seller=seller)
    offer.status = 'Rejected'
    offer.save()
    return redirect('seller_dash')
