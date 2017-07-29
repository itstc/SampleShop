from django import forms

SMALL = 'S'
MEDIUM = 'M'
LARGE = 'L'
PRODUCT_QUANTITY_CHOICES = (
    (SMALL, 'Small'),
    (MEDIUM, 'Medium'),
    (LARGE, 'Large'),
)

class CartAddProductForm(forms.Form):
    size = forms.ChoiceField(choices=PRODUCT_QUANTITY_CHOICES)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)