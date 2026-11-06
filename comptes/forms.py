"""
comptes/forms.py : Formulaires Django sécurisés pour l'inscription et la connexion.

Conforme au cahier des charges :
- Validation des saisies utilisateur.
- Hachage automatique des mots de passe avec l'algorithme standard PBKDF2/SHA256.
- Attribution du rôle (PATIENT par défaut ou ADMINISTRATEUR).

=== ÉTAT D'AVANCEMENT ===
[✅ FAIT] InscriptionForm : hérite de UserCreationForm, hachage automatique du mot de passe,
          champs Prénom, Nom, Email, Rôle, contrôle de l'unicité de l'email.
[✅ FAIT] ConnexionForm : hérite de AuthenticationForm, vérifie les identifiants.

[❌ RESTE À FAIRE] Pas de formulaire de modification de profil utilisateur (Nom, Email).
[❌ RESTE À FAIRE] Pas de formulaire de changement de mot de passe.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class InscriptionForm(UserCreationForm):
    """
    Formulaire d'inscription pour les nouveaux utilisateurs.
    Hérite de UserCreationForm pour garantir le hachage sécurisé du mot de passe
    et la double confirmation.
    """
    first_name = forms.CharField(
        max_length=150, 
        required=True, 
        label="Prénom",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jean'})
    )
    last_name = forms.CharField(
        max_length=150, 
        required=True, 
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dupont'})
    )
    email = forms.EmailField(
        required=True, 
        label="Adresse email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'jean.dupont@exemple.fr'})
    )
    role = forms.ChoiceField(
        choices=CustomUser.Role.choices,
        initial=CustomUser.Role.PATIENT,
        label="Rôle du compte",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'role')

    def clean_email(self):
        """Vérifie l'unicité de l'adresse email pour la sécurité des comptes."""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà associée à un compte.")
        return email


class ConnexionForm(AuthenticationForm):
    """
    Formulaire d'authentification avec vérification des identifiants et protection de session.
    """
    username = forms.CharField(
        label="Identifiant ou Email",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre identifiant'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'})
    )
