"""
evaluations/views.py : Vues pour le questionnaire, les résultats et l'historique.

Rôle dans le projet :
- vue_questionnaire(request) :
    * Protégée par @login_required (seul un patient connecté y accède).
    * Affiche le formulaire WHO-5 (GET).
    * Calcule les scores, sauvegarde l'Evaluation, déclenche ServiceIA_Ollama et crée le PlanPedagogique (POST).
- vue_resultats(request, evaluation_id) :
    * Affiche le score sur 100, l'avertissement médical et le plan 7 jours.
    * Vérifie que l'évaluation appartient bien à l'utilisateur connecté (protection des données).
- vue_historique(request) :
    * Liste chronologique de toutes les évaluations du patient connecté.
"""

