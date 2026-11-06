"""
evaluations/models.py : Modélisation des questionnaires WHO-5 et des plans pédagogiques.

Conforme au diagramme de classes UML :
- Evaluation : enregistre les réponses (0 à 5), calcule le score brut (/25) et le score sur 100 (* 4).
- PlanPedagogique : stocke le programme 7 jours produit par l'IA et l'avertissement médical.
"""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Evaluation(models.Model):
    """
    Modèle représentant une passation du questionnaire WHO-5 par un patient.
    """
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name="Patient"
    )
    dateEvaluation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de l'évaluation"
    )

    # Les 5 réponses officielles (valeurs de 0 à 5 selon l'échelle de Likert OMS)
    reponseQ1 = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Q1 : Gai(e) et de bonne humeur"
    )
    reponseQ2 = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Q2 : Calme et détendu(e)"
    )
    reponseQ3 = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Q3 : Actif/ve et vigoureux/se"
    )
    reponseQ4 = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Q4 : Réveillé(e) frais/fraîche et dispos(e)"
    )
    reponseQ5 = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Q5 : Vie quotidienne remplie de choses intéressantes"
    )

    # Scores calculés
    scoreBrut = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Score brut (0 - 25)"
    )
    scoreSur100 = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Score sur 100"
    )

    class Meta:
        ordering = ['-dateEvaluation']
        verbose_name = "Évaluation WHO-5"
        verbose_name_plural = "Évaluations WHO-5"

    def calculerScoreTotal(self) -> int:
        """Calcule la somme des 5 réponses (score brut compris entre 0 et 25)."""
        return sum([
            self.reponseQ1 or 0,
            self.reponseQ2 or 0,
            self.reponseQ3 or 0,
            self.reponseQ4 or 0,
            self.reponseQ5 or 0,
        ])

    def calculerScoreSur100(self) -> int:
        """Calcule le score normalisé sur 100 (Score brut x 4)."""
        return self.calculerScoreTotal() * 4

    def save(self, *args, **kwargs):
        """Met à jour automatiquement les scores avant sauvegarde."""
        self.scoreBrut = self.calculerScoreTotal()
        self.scoreSur100 = self.calculerScoreSur100()
        super().save(*args, **kwargs)

    def __str__(self):
        date_str = self.dateEvaluation.strftime('%d/%m/%Y') if self.dateEvaluation else 'En cours'
        return f"Évaluation #{self.id} de {self.patient} ({self.scoreSur100}/100 - {date_str})"


class PlanPedagogique(models.Model):
    """
    Modèle représentant le plan d'accompagnement éducatif de bien-être sur 7 jours
    associé à une évaluation donnée.
    """
    AVERTISSEMENT_PAR_DEFAUT = (
        "Cet outil éducatif repose sur des données fictives et ne constitue en aucun cas "
        "un diagnostic médical, ni une recommandation thérapeutique. Pour tout avis médical, "
        "consultez un professionnel de santé."
    )

    evaluation = models.OneToOneField(
        Evaluation,
        on_delete=models.CASCADE,
        related_name='plan',
        verbose_name="Évaluation associée"
    )
    dateGeneration = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de génération"
    )
    contenuTexte = models.TextField(
        verbose_name="Plan de bien-être sur 7 jours"
    )
    avertissementMedical = models.TextField(
        default=AVERTISSEMENT_PAR_DEFAUT,
        verbose_name="Avertissement médical obligatoire"
    )

    class Meta:
        verbose_name = "Plan Pédagogique"
        verbose_name_plural = "Plans Pédagogiques"

    def afficherPlan(self) -> str:
        """Retourne le plan structuré avec son avertissement médical."""
        return f"{self.contenuTexte}\n\n[AVERTISSEMENT MÉDICAL]\n{self.avertissementMedical}"

    def __str__(self):
        return f"Plan pour Évaluation #{self.evaluation_id}"
