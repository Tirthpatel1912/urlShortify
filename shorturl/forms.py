from django import forms
from .models import ShortURL
from django.core.exceptions import ValidationError
from datetime import datetime

class URLShortenerForm(forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = ['long_url','slug','expiration_date', 'is_private', 'password']
        labels = {
            'long_url': 'Enter the Long URL',
            'slug': 'Custom Alias',
            'is_private': 'Make this URL Private?',
            'password': 'Password for Private URL',
            'expiration_date': 'Expiration Date',
        }
        widgets = {
            'long_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter the long URL'}),
            'expiration_date': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the alias of url'}),
            'is_private': forms.CheckboxInput(attrs={'id': 'id_is_private'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password (if private)', 'id': 'id_password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not isinstance(cleaned_data, dict):
            raise forms.ValidationError("Internal error: Form data is not properly structured.")
        slug = self.cleaned_data.get('slug')
        long_url = cleaned_data.get('long_url')
        is_private = cleaned_data.get('is_private')
        password = cleaned_data.get('password')
        expiration_date = cleaned_data.get('expiration_date')

        print(f"Long URL: {long_url}, Is Private: {is_private}")
        # If the URL is private, ensure a password is provided
        if is_private and not password:
            self.add_error('password', 'Password is required for private URLs.')

        # Ensure an expiration date is provided for all URLs
        if not expiration_date:
            self.add_error('expiration_date', 'Expiration date is required for all URLs.')

        # Optional: Check if expiration date is in the past
        if expiration_date and expiration_date < datetime.now().date():
            self.add_error('expiration_date', 'Expiration date cannot be in the past.')

        # If slug is exist
        if ShortURL.objects.filter(slug=slug).exists():
            raise forms.ValidationError('This alias is already in use. Please choose another one.')

        return cleaned_data

