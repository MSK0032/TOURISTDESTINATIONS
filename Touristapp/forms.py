from django import forms
from .models import TouristDestination, TouristImage

class TouristDestinationForm(forms.ModelForm):
    tourist_img = forms.ImageField()


    class Meta:
        model = TouristDestination
        exclude = ['created_at', 'updated_at']

class TouristImageForm(forms.ModelForm):
    class Meta:
        model = TouristImage
        fields = ['Tourist_img']  # Only include the image field
