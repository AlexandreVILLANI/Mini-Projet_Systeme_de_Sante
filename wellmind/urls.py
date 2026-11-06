"""
wellmind/urls.py : Routeur d'URL racine du projet WellMind-Lab.
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
