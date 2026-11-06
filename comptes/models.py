"""
comptes/models.py : Modélisation des comptes utilisateurs.

Conforme au diagramme UML :
- Classe Compte (ici CustomUser héritant d'AbstractUser)
- Attributs : nom, email, motDePasse, dateCreation, role
- Rôles : PATIENT, ADMINISTRATEUR

=== ÉTAT D'AVANCEMENT ===
[✅ FAIT] Classe CustomUser définie avec les champs nom, email, role (PATIENT / ADMINISTRATEUR)
[✅ FAIT] Héritage de AbstractUser (gestion des mots de passe, sessions, permissions)
[✅ FAIT] Méthodes est_patient() et est_admin()
[✅ FAIT] Migration de la base de données générée et appliquée (comptes/migrations/0001_initial.py)
[✅ FAIT] Déclaré comme AUTH_USER_MODEL dans settings.py

[❌ RESTE À FAIRE] Pas de vue de profil utilisateur (édition du nom, email, mot de passe)
[❌ RESTE À FAIRE] Pas de réinitialisation de mot de passe
[❌ RESTE À FAIRE] Pas de gestion des comptes Administrateur côté interface (CRUD)
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        PATIENT = 'PATIENT', 'Patient'
        ADMINISTRATEUR = 'ADMINISTRATEUR', 'Administrateur'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PATIENT,
        verbose_name="Rôle",
        help_text="Définit si l'utilisateur est un patient ou un administrateur."
    )

    def est_patient(self):
        """Vérifie si le compte est un patient."""
        return self.role == self.Role.PATIENT

    def est_admin(self):
        """Vérifie si le compte est un administrateur."""
        return self.role == self.Role.ADMINISTRATEUR or self.is_staff

    def __str__(self):
        nom_affiche = self.get_full_name() or self.username
        return f"{nom_affiche} ({self.get_role_display()})"
