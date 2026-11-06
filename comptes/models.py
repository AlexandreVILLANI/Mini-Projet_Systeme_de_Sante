"""
comptes/models.py : Modélisation des données des utilisateurs.

Rôle dans le projet :
- Définit la classe 'CustomUser' héritant de 'django.contrib.auth.models.AbstractUser'.
- Intègre les spécifications du diagramme UML :
    * email : Identifiant unique
    * nom / prenom : Identité de l'utilisateur
    * role : Choix entre 'PATIENT' et 'ADMINISTRATEUR'
    * dateCreation : Date automatique de création
- Gère la méthode pour vérifier si l'utilisateur est un patient ou un administrateur.
"""

