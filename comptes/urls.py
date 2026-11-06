"""
comptes/urls.py : Déclaration des routes de l'application 'comptes'.
"""
from django.urls import path
from . import views

app_name = 'comptes'

urlpatterns = [
    path('inscription/', views.vue_inscription, name='inscription'),
    path('connexion/', views.vue_connexion, name='connexion'),
    path('deconnexion/', views.vue_deconnexion, name='deconnexion'),
]
