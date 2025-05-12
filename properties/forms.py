from django import forms
from .models import PurchaseOffer

class PurchaseOfferForm(forms.ModelForm):
    class Meta:
        model = PurchaseOffer
        fields = ['offer_amount', 'expiration_date']
        widgets = {
            'offer_amount': forms.NumberInput(attrs={'type': 'number', 'class': 'input', 'placeholder': 'Amount'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date', 'class': 'input', 'placeholder': 'Expiration date'}),
        }
