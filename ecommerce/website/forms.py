from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('P', 'PayPal'),
    ('C', 'Credit Card'),
    ('D', 'Cash on Delivery')
)
class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'ABC Street'}))
    country = CountryField(blank_label='(select country)').formfield(widget = CountrySelectWidget(attrs={'class':'country-select'}))
    city = forms.CharField()
    zip = forms.CharField()
    phone = forms.CharField()
    ship_to_different_address = forms.BooleanField(widget=forms.CheckboxInput())
    payment_method =forms.ChoiceField(widget=forms.RadioSelect(),choices=PAYMENT_CHOICES)
