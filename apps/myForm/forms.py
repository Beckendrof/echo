from django import forms
from .models import User, Creator, Editor

# forms.py
class UserRegistrationForm(forms.Form):
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent',
            'placeholder': 'you@example.com'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent',
            'placeholder': '••••••••'
        })
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent',
            'placeholder': '••••••••'
        })
    )
    user_type = forms.ChoiceField(
        label="User Type",
        choices=[('', 'Choose an option'), ('creator', 'Creator'), ('editor', 'Editor')],
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent pr-8'
        })
    )
    youtube_channel = forms.CharField(
        label="YouTube Channel ID",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent hidden',
            'placeholder': 'Enter your YouTube channel ID',
            'id': 'id_youtube_channel'
        })
    )
    brand_name = forms.CharField(
        label="Brand Name",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent hidden',
            'placeholder': 'Enter your brand name',
            'id': 'id_brand_name'
        })
    )
    display_name = forms.CharField(
        label="Display Name",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent hidden',
            'placeholder': 'Enter your display name',
            'id': 'id_display_name'
        })
    )
    expertise_tags = forms.CharField(
        label="Expertise Tags",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent hidden',
            'placeholder': 'Enter your expertise tags (comma-separated)',
            'id': 'id_expertise_tags'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        user_type = cleaned_data.get('user_type')
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        

        if user_type == 'creator':
            if not cleaned_data.get('youtube_channel') or not cleaned_data.get('brand_name'):
                raise forms.ValidationError("YouTube Channel ID and Brand Name are required for Creators.")
        elif user_type == 'editor':
            if not cleaned_data.get('display_name') or not cleaned_data.get('expertise_tags'):
                raise forms.ValidationError("Display Name and Expertise Tags are required for Editors.")

        return cleaned_data

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={
            "id": "email",
            "class": "w-full px-3 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent",
            "placeholder": "you@example.com"
        })
    )
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "id": "password",
            "class": "w-full px-3 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 focus:border-transparent",
            "placeholder": "••••••••"
        })
    )
    
    remember_me = forms.BooleanField(
        label="Remember me",
        required=False,
        widget=forms.CheckboxInput(attrs={
            "id": "remember_me",
            "class": "h-4 w-4 text-gray-900 border-gray-300 rounded focus:ring-gray-400"
        })
    )