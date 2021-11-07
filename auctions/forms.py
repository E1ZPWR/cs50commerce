from django.forms import ModelForm
from django import forms

from .models import Category, Listing


class CreateCatgoryForm(forms.Form):
    # Catgory Title
    category = forms.CharField(label="Title")


class CreateListingForm(forms.Form):
    # Item Title
    title = forms.CharField(label="Title", widget=forms.TextInput(
        attrs={'class': 'form-control',
               'autofocus': 'on',
               "name": "item_name",
               "placeholder": "Item Name"
               }))
    # Item Description
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control',
               "name": "description",
               "style":
                   {"width": "100%",
                    "vertical-align": "top",
                    "height": "100%"
                    },
               "placeholder": "Enter Your Descriptions"
               }))
    # Item Start Price
    bid = forms.CharField(widget=forms.NumberInput(
        attrs={'class': 'form-control',
               'autofocus': 'on',
               "name": "bid_price",
               "placeholder": "Starting Price",
               'step': '100',
               'min': '0'
               }))
    # Item URL Link
    image_url = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'autofocus': 'on',
               "name": "image_url",
               "placeholder": "img url addr",
               "id": "basic-url",
               "value": "https://picsum.photos/seed/picsum/300/300"
               }))
