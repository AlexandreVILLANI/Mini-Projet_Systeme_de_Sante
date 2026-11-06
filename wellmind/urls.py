"""
wellmind/urls.py : Routeur racine de l'application web.

Rôle dans le projet :
- Distribue les requêtes entrantes vers les sous-applications :
    * include('comptes.urls') : routes pour l'inscription, connexion, déconnexion.
    * include('evaluations.urls') : routes pour le questionnaire WHO-5, résultats et historique.
    * path('admin/', admin.site.urls) : interface d'administration Django.
- Définit la page d'accueil principale du site (redirection ou vue de présentation).
"""

