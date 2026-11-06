"""
comptes/forms.py : Formulaires Django pour la gestion des utilisateurs.

Rôle dans le projet :
- Formulaire d'inscription (ex: InscriptionForm héritant de UserCreationForm) :
    * Validation des champs (nom, email, mot de passe).
    * Hachage automatique et sécurisé du mot de passe.
    * Attribution automatique du rôle 'PATIENT' par défaut.
- Formulaire de connexion (ex: ConnexionForm héritant de AuthenticationForm) :
    * Vérification de l'authentification et gestion des erreurs de saisie.
"""

