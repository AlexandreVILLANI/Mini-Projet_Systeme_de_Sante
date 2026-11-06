"""
comptes/admin.py : Configuration de l'interface d'administration pour les comptes.

=== ÉTAT D'AVANCEMENT ===
[✅ FAIT] CustomUser enregistré avec une classe UserAdmin étendue affichant le champ 'role'.
[✅ FAIT] Interface admin accessible via /admin/ avec filtrage par rôle.

[❌ RESTE À FAIRE] Méthodes listerComptes / modifierCompte / supprimerCompte du diagramme UML
          à implémenter si on veut une interface dédiée côté Patient/Administrateur
          (en dehors du panneau /admin/ Django standard).
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    # Ajoute le champ 'role' dans le formulaire d'édition de l'admin
    fieldsets = UserAdmin.fieldsets + (
        ('Rôle WellMind', {'fields': ('role',)}),
    )

