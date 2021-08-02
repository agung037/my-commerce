from django import forms
from .models import Categories

class CreateListingForm(forms.Form):
    name = forms.CharField(label='Title', max_length=100)
    categories = forms.ModelChoiceField(queryset=Categories.objects.all())
    price = forms.DecimalField(label='Price')
    image = forms.URLField(label='Image Url', required=False)
    description = forms.CharField(label="Description", widget=forms.Textarea)