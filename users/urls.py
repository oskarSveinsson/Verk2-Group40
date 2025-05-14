from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView
from users.views import purchase_offers

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('my-offers/', purchase_offers, name='purchase_offers'),
    path('seller/', views.seller_dash, name='seller_dash'),
    path('seller/accept/<int:offer_id>', views.accept_offer, name='accept_offer'),
    path('seller/decline/<int:offer_id>', views.decline_offer, name='decline_offer'),
]