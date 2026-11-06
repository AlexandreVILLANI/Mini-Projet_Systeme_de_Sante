"""
comptes/views.py : Contrôleurs pour l'inscription, la connexion et la déconnexion.

Sécurité mise en œuvre :
- Mots de passe hachés à l'enregistrement (PBKDF2/SHA256).
- Gestion des sessions utilisateur authentifiées.
- Validation stricte des formulaires côté serveur.
- Protection contre les attaques CSRF.

=== ÉTAT D'AVANCEMENT ===
[✅ FAIT] vue_inscription : formulaire InscriptionForm validé, hachage du mot de passe, enregistrement
          en base de données, redirection vers la connexion avec message de succès.
[✅ FAIT] vue_connexion : AuthenticationForm, login() Django (session), redirection vers ?next=.
[✅ FAIT] vue_deconnexion : logout() Django, destruction de la session.
[✅ FAIT] Si déjà connecté, l'utilisateur est redirigé directement vers le questionnaire.

[❌ RESTE À FAIRE] Pas de vue d'administration : liste des comptes, modification, suppression
          (côté Administrateur, méthodes listerComptes, ajouterCompte, modifierCompte,
          supprimerCompte du diagramme UML).
[❌ RESTE À FAIRE] Pas de gestion du rôle Administrateur dans la navigation (accès différencié).
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import InscriptionForm, ConnexionForm


def vue_inscription(request):
    """
    Traitement sécurisé de l'inscription d'un nouvel utilisateur.
    """
    if request.user.is_authenticated:
        return redirect('evaluations:questionnaire')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 
                f"Compte {user.username} créé avec succès ! Connectez-vous pour commencer votre évaluation."
            )
            return redirect('comptes:connexion')
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier vos informations.")
    else:
        form = InscriptionForm()

    return render(request, 'comptes/inscription.html', {'form': form})


def vue_connexion(request):
    """
    Authentification sécurisée et ouverture de session utilisateur.
    """
    if request.user.is_authenticated:
        return redirect('evaluations:questionnaire')

    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Connexion réussie ! Bienvenue {user.first_name or user.username}.")
            
            # Redirection vers la page demandée ou vers le questionnaire par défaut
            prochaine_page = request.GET.get('next')
            if prochaine_page:
                return redirect(prochaine_page)
            return redirect('evaluations:questionnaire')
        else:
            messages.error(request, "Identifiant ou mot de passe incorrect.")
    else:
        form = ConnexionForm()

    return render(request, 'comptes/connexion.html', {'form': form})


def vue_deconnexion(request):
    """
    Fermeture sécurisée de la session utilisateur.
    """
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('comptes:connexion')
