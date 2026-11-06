"""
comptes/views.py : Vues pour l'inscription, la connexion et la déconnexion.
"""
from django.shortcuts import render, redirect
from django.contrib import messages


def vue_inscription(request):
    """Vue du formulaire d'inscription."""
    if request.method == 'POST':
        # En mode démonstration front-end : simule la création de compte
        messages.success(request, "Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
        return redirect('comptes:connexion')
    return render(request, 'comptes/inscription.html')


def vue_connexion(request):
    """Vue du formulaire de connexion."""
    if request.method == 'POST':
        # En mode démonstration front-end : simule l'authentification et redirige vers le test
        messages.success(request, "Connexion réussie ! Bienvenue sur WellMind-Lab.")
        return redirect('evaluations:questionnaire')
    return render(request, 'comptes/connexion.html')


def vue_deconnexion(request):
    """Déconnexion de l'utilisateur."""
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('comptes:connexion')
