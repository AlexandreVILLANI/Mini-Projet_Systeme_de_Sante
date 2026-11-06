"""
tests/test_ia.py : Tests unitaires pour l'intégration de l'IA (Ollama) et le fallback.

Rôle dans le projet :
- Tester la génération du prompt système sans recommandation médicale.
- Tester le comportement de secours (fallback) si le serveur Ollama est inaccessible (simulation d'erreur réseau).
- Vérifier que l'avertissement médical est systématiquement présent dans le PlanPedagogique.
"""

