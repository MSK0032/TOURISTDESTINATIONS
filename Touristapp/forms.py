from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django import forms

class TouristDestinationForm(forms.ModelForm):
    class Meta:
        model = TouristDestination
        fields = ['place_name', 'description', 'location_state', 'location_district', 'weather', 'google_map_link', 'tourist_img']


class TouristDestinationImageForm(forms.ModelForm):
    class Meta:
        model = TouristImage
        fields = ['Tourist_img']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

class LoginForm(AuthenticationForm):
    pass


