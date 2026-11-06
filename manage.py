#!/usr/bin/env python
"""
manage.py : Utilitaire en ligne de commande de Django.

Rôle dans le projet :
- Point d'entrée pour exécuter les commandes d'administration Django.
- Exemples de commandes courantes :
    * python manage.py runserver : Démarre le serveur web de développement local.
    * python manage.py makemigrations : Détecte les modifications dans models.py et prépare les migrations.
    * python manage.py migrate : Applique les migrations à la base de données SQLite.
    * python manage.py createsuperuser : Crée un compte administrateur Django.
    * python manage.py test : Lance la suite de tests.
"""
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wellmind.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossible d'importer Django. Avez-vous pensé à activer votre "
            "environnement virtuel avec 'source venv/bin/activate' ?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
