from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

class InscriptionForm(forms.Form):
    nom = forms.CharField(label="Nom", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Votre nom','class': 'inputChamp'}))
    prenom = forms.CharField(label="Prenom", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Votre pseudo','class': 'inputChamp'}))
    email = forms.EmailField(label="Email", max_length=200, widget=forms.EmailInput(attrs={'placeholder': 'Votre email','class': 'inputChamp'}))
    mot_de_passe = forms.CharField(label="Mot de passe", max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Votre mot de passe','class': 'inputChamp'}))
    ville = forms.CharField(label="Ville", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Votre ville','class': 'inputChamp'}))
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data.get("mot_de_passe")
    
    def clean_pseudo(self):
        pseudo = self.cleaned_data['pseudo']
        if len(pseudo) < 5:
            raise ValidationError("Le pseudo doit faire au moins 5 caractères")
        return pseudo
    
    def clean_data(self):
        cleaned_data = super().clean()
        return cleaned_data.get("email")