"""
comptes/views.py : Contrôleurs pour la gestion des utilisateurs et sessions.

Rôle dans le projet :
- vue_inscription(request) : Traite le formulaire d'inscription et enregistre le patient.
- vue_connexion(request) : Authentifie l'utilisateur, ouvre la session Django et redirige
  vers le questionnaire WHO-5 ou l'historique.
- vue_deconnexion(request) : Ferme la session utilisateur et redirige vers la page d'accueil.
"""

