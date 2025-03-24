from django import forms
from .models import User, Creator, Editor

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password', 'user_type']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

class CreatorForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = ['youtube_channel', 'brand_name']

class EditorForm(forms.ModelForm):
    expertise_tags = forms.CharField(help_text="Enter tags separated by commas")

    class Meta:
        model = Editor
        fields = ['display_name', 'expertise_tags']

    def clean_expertise_tags(self):
        tags = self.cleaned_data['expertise_tags']
        return [tag.strip() for tag in tags.split(',')]

class CombinedRegistrationForm(UserRegistrationForm):
    youtube_channel = forms.CharField(required=False)
    brand_name = forms.CharField(required=False)
    display_name = forms.CharField(required=False)
    expertise_tags = forms.CharField(required=False, help_text="Enter tags separated by commas")

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')

        if user_type == 'creator':
            if not cleaned_data.get('youtube_channel') or not cleaned_data.get('brand_name'):
                raise forms.ValidationError("YouTube channel and brand name are required for creators")
        elif user_type == 'editor':
            if not cleaned_data.get('display_name') or not cleaned_data.get('expertise_tags'):
                raise forms.ValidationError("Display name and expertise tags are required for editors")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        if user.user_type == 'creator':
            Creator.objects.create(
                user=user,
                youtube_channel=self.cleaned_data['youtube_channel'],
                brand_name=self.cleaned_data['brand_name']
            )
        elif user.user_type == 'editor':
            Editor.objects.create(
                user=user,
                display_name=self.cleaned_data['display_name'],
                expertise_tags=self.cleaned_data['expertise_tags'].split(',')
            )

        return user
