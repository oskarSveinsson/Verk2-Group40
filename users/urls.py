from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('my-offers/', views.purchase_offers, name='purchase_offers'),
    path('register/', views.register, name='register'),
]