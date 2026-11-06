"""
evaluations/forms.py : Formulaire pour le questionnaire officiel OMS WHO-5.

Rôle dans le projet :
- Formulaire Django (ex: QuestionnaireWHO5Form) :
    * Propose 5 champs (Q1 à Q5) avec widgets de type RadioSelect.
    * Échelle de Likert officielle (0 = À aucun moment ... 5 = Tout le temps).
    * Validation des bornes [0 - 5] et obligation de répondre à toutes les questions.
"""

