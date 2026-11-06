"""
wellmind/settings.py : Configuration centrale du projet Django.

Rôle dans le projet :
- Déclare les applications installées (INSTALLED_APPS) : y ajouter 'comptes' et 'evaluations'.
- Définit le modèle utilisateur personnalisé : AUTH_USER_MODEL = 'comptes.CustomUser'.
- Configure la base de données relationnelle (par défaut SQLite pour le TP).
- Configure le moteur de templates (répertoire 'templates/' global).
- Définit la gestion des fichiers statiques (CSS, JS dans 'static/').
- Gère la sécurité des sessions et de l'authentification.
"""

