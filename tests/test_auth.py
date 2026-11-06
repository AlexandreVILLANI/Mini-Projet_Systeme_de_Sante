"""
tests/test_auth.py : Tests unitaires pour la sécurité, l'inscription et les sessions.

Rôle dans le projet :
- Vérifier que les mots de passe sont bien hachés en base et jamais stockés en clair.
- Tester qu'un utilisateur non connecté ne peut pas accéder aux pages protégées (redirection vers login).
- Tester qu'un patient ne peut consulter que son propre historique (isolation des données de santé).
"""

