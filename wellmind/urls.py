"""
wellmind/urls.py : Routeur d'URL racine du projet WellMind-Lab.

=== ÉTAT D'AVANCEMENT ===
[✅ FAIT] Route racine '/' redirige vers la page de connexion (accueil dynamique).
[✅ FAIT] Interface admin Django disponible sur /admin/.
[✅ FAIT] Routes 'comptes/' (inscription, connexion, déconnexion) incluses via comptes.urls.
[✅ FAIT] Routes 'evaluations/' (questionnaire, résultats, historique) incluses via evaluations.urls.

[❌ RESTE À FAIRE] Page d'accueil dédiée (vue HTML) si on veut un landing page au lieu d'une redirection.
[❌ RESTE À FAIRE] Routes API REST (si extension future vers mobile ou SPA).
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Redirection de la racine vers la page de connexion ou questionnaire
    path('', RedirectView.as_view(pattern_name='comptes:connexion', permanent=False), name='accueil'),

    # Interface d'administration Django (gestion des comptes, évaluations, etc.)
    path('admin/', admin.site.urls),

    # Applications métiers
    path('comptes/', include('comptes.urls')),
    path('evaluations/', include('evaluations.urls')),
]
