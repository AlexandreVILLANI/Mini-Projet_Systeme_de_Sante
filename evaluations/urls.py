"""
evaluations/urls.py : Déclaration des routes de l'application 'evaluations'.
"""
from django.urls import path
from . import views

app_name = 'evaluations'

urlpatterns = [
    path('questionnaire/', views.vue_questionnaire, name='questionnaire'),
    path('resultats/<int:evaluation_id>/', views.vue_resultats, name='resultats'),
    path('historique/', views.vue_historique, name='historique'),
]
