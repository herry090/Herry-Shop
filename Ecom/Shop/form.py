import re
from django import forms
from django.contrib.auth.models import User
from .models import CustomUser, Contact

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmer le mot de passe')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'profile_image', 'password', 'confirm_password']  # Ajout des champs de mot de passe
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'required': False}),  # Rendre le champ facultatif
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Validation de la complexité du mot de passe
        if password:
            if len(password) < 8:
                raise forms.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
            if not re.search(r"[A-Z]", password):
                raise forms.ValidationError("Le mot de passe doit contenir au moins une majuscule.")
            if not re.search(r"[a-z]", password):
                raise forms.ValidationError("Le mot de passe doit contenir au moins une minuscule.")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                raise forms.ValidationError("Le mot de passe doit contenir au moins un caractère spécial.")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
    
class LocationForm(forms.Form):
    country = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    region = forms.CharField(widget=forms.Textarea, required=False)

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image']