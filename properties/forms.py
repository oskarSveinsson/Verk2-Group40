from django import forms
from .models import PurchaseOffer

class TailwindMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm '
                         'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            })


class PurchaseOfferForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = PurchaseOffer
        fields = ['offer_amount', 'expiration_date']
        widgets = {
            'offer_amount': forms.NumberInput(attrs={'type': 'number', 'class': 'input', 'placeholder': 'Amount'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date', 'class': 'input', 'placeholder': 'Expiration date'}),
        }

class ContactForm(TailwindMixin, forms.Form):
    street = forms.CharField(label='Street', max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=5)
    country = forms.CharField(max_length=100)
    national_id = forms.CharField(label='National ID', max_length=10)

class PaymentChoiceForm(TailwindMixin, forms.Form):
    PAYMENT_METHODS = [
        ('CreditCard', 'Credit Card'),
        ('BankTransfer', 'Bank Transfer'),
        ('Mortgage', 'Mortgage'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_METHODS)

class CreditCardForm(TailwindMixin, forms.Form):
    card_holder = forms.CharField(label='Cardholder name', max_length=100)
    card_number = forms.CharField(label='Card number', max_length=100)
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    cvc = forms.CharField(label='CVC', max_length=5)

class BankTransferForm(TailwindMixin, forms.Form):
    account_number = forms.CharField(label='Account number', max_length=50)

class MortgageForm(TailwindMixin, forms.Form):
    MORTGAGE_PROVIDER = [
        ('Arion', 'Arion Banki'),
        ('Landsbankinn', 'Landsbankinn'),
        ('Islandsbanki', 'Íslandsbanki'),
        ('Sparisjodurinn', 'Sparisjóðurinn'),
    ]
    mortgage_provider = forms.ChoiceField(choices=MORTGAGE_PROVIDER)