from django.core.exceptions import ValidationError
from django import forms
from .models import Ville, Joueur

class InscriptionForm(forms.ModelForm):
    nom = forms.CharField(label="Nom", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Votre nom','class': 'inputChamp'}))
    prenom = forms.CharField(label="Prenom", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Votre pseudo','class': 'inputChamp'}))
    email = forms.EmailField(label="Email", max_length=200, widget=forms.EmailInput(attrs={'placeholder': 'Votre email','class': 'inputChamp'}))
    mot_de_passe = forms.CharField(label="Mot de passe", max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Votre mot de passe','class': 'inputChamp'}))
    ville = forms.ModelChoiceField(label="Ville", queryset=Ville.objects.all(), widget=forms.Select(attrs={'class': 'inputChamp'}))

    class Meta:
        model = Joueur
        fields = ['nom', 'prenom', 'email', 'mot_de_passe', 'ville']