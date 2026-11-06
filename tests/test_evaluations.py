"""
tests/test_evaluations.py : Tests unitaires (Pytest) pour le calcul du score WHO-5.

Rôle dans le projet :
- Vérifier que la somme des 5 réponses donne exactement le score brut attendu (0 à 25).
- Vérifier la formule du score sur 100 : scoreSur100 = scoreBrut * 4.
- Tester les cas limites : score minimal (0) et score maximal (100).
- Tester la validation des réponses (rejeter les valeurs inférieures à 0 ou supérieures à 5).
"""

