"""
evaluations/admin.py : Configuration de l'administration pour les évaluations et plans.

Rôle dans le projet :
- Permet aux administrateurs de consulter les évaluations et les plans générés dans l'interface admin.

=== ÉTAT D'AVANCEMENT ===
[✅ FAIT] Evaluation et PlanPedagogique enregistrés dans l'interface admin Django (/admin/).
[✅ FAIT] Liste des évaluations visible par l'administrateur via list_display.

[❌ RESTE À FAIRE] Méthodes UML Administrateur.listerComptes() / ajouterCompte() /
          modifierCompte() / supprimerCompte() — uniquement gérées via /admin/ Django pour l'instant.
          À implémenter en vues web dédiées si le TP l'exige.
[❌ RESTE À FAIRE] Filtres et actions personnalisées dans EvaluationAdmin (ex. export CSV).
"""
from django.contrib import admin
from .models import Evaluation, PlanPedagogique


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'scoreBrut', 'scoreSur100', 'dateEvaluation')
    list_filter = ('dateEvaluation',)
    ordering = ('-dateEvaluation',)
    search_fields = ('patient__username',)


@admin.register(PlanPedagogique)
class PlanPedagogiqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'evaluation', 'dateGeneration')
    ordering = ('-dateGeneration',)

