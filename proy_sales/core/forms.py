from django import forms
from core.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['description','price','stock','brand','categories','line','supplier','expiration_date','image','state']
