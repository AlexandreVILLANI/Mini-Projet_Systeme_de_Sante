"""
evaluations/models.py : Modélisation des questionnaires WHO-5 et des plans pédagogiques.

Rôle dans le projet :
- Classe 'Evaluation' :
    * Relation ForeignKey vers CustomUser (un patient a 0..* évaluations).
    * Champs reponseQ1 à reponseQ5 (entiers de 0 à 5).
    * dateEvaluation : DateTimeField automatique.
    * scoreBrut : somme des 5 réponses (0 à 25).
    * scoreSur100 : scoreBrut * 4 (0 à 100).
    * Méthodes métier : calculerScoreTotal(), calculerScoreSur100(), save().
- Classe 'PlanPedagogique' :
    * Relation OneToOneField avec 'Evaluation' (1 évaluation génère 1 plan).
    * contenuTexte : contenu du plan de bien-être sur 7 jours généré par l'IA ou le fallback.
    * avertissementMedical : mention légale obligatoire (données fictives, éducatif, pas de diagnostic).
    * dateGeneration : DateTimeField automatique.
"""

