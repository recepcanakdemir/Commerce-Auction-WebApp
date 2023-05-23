from django import forms
from .models import Listing


class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = [
            'name',
            'price',
            'description',
            'category',
            'image',
        ]