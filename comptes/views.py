"""
comptes/views.py : Vues pour l'inscription, la connexion et la déconnexion.
"""
from django.shortcuts import render, redirect
from django.contrib import messages


def vue_inscription(request):
    """Vue du formulaire d'inscription."""
    if request.method == 'POST':
        # =========================================================================
        # [TEMPORAIRE - NE PAS GARDER POUR LA VERSION FINALE DU PROJET]
        # Ce bloc simule l'inscription pour tester l'interface graphique.
        # TODO FINALE :
        # 1. Utiliser le formulaire Django 'InscriptionPatientForm(request.POST)'.
        # 2. Vérifier 'if form.is_valid():'.
        # 3. Enregistrer l'utilisateur avec 'user = form.save()'.
        # 4. Rediriger vers la connexion ou connecter automatiquement avec 'login(request, user)'.
        # =========================================================================
        messages.success(request, "Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
        return redirect('comptes:connexion')
    return render(request, 'comptes/inscription.html')


def vue_connexion(request):
    """Vue du formulaire de connexion."""
    if request.method == 'POST':
        # =========================================================================
        # [TEMPORAIRE - NE PAS GARDER POUR LA VERSION FINALE DU PROJET]
        # Ce bloc simule la connexion sans vérifier le mot de passe réel.
        # TODO FINALE :
        # 1. Utiliser 'AuthenticationForm(request, data=request.POST)' ou 'authenticate()'.
        # 2. Vérifier les identifiants et le mot de passe haché.
        # 3. Ouvrir la session avec 'login(request, user)'.
        # 4. Rediriger selon le rôle (Patient -> questionnaire, Admin -> gestion).
        # =========================================================================
        messages.success(request, "Connexion réussie ! Bienvenue sur WellMind-Lab.")
        return redirect('evaluations:questionnaire')
    return render(request, 'comptes/connexion.html')


def vue_deconnexion(request):
    """Déconnexion de l'utilisateur."""
    # =========================================================================
    # [TEMPORAIRE - NE PAS GARDER POUR LA VERSION FINALE DU PROJET]
    # TODO FINALE :
    # Appeler 'from django.contrib.auth import logout' puis 'logout(request)'
    # pour détruire réellement la session utilisateur en cours.
    # =========================================================================
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('comptes:connexion')
