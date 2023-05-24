from django import forms
from .models import Listing,Comment,Bid


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
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.URLInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = [
            'title',
            'content',
            
        ]
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.TextInput(attrs={'class':'form-control'}),
        }


class BidForm(forms.ModelForm):

    class Meta: 
        model = Bid
        fields = [
             'price',
        ]
        widgets = {
            'price':forms.NumberInput(attrs={'class':'form-control'}),
        }