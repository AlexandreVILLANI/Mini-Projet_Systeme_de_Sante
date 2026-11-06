"""
tests/test_evaluations.py : Tests unitaires pour le calcul des scores WHO-5.

Exigences du sujet :
- Score = 4 x somme des cinq réponses (0 à 5).
- Score brut compris entre 0 et 25.
- Score normalisé compris entre 0 et 100.
"""
from django.test import TestCase
from evaluations.models import Evaluation
from comptes.models import CustomUser


class TestCalculScoreWHO5(TestCase):
    """Suite de tests pour la validation des calculs de scores WHO-5."""

    def setUp(self):
        """Initialise un utilisateur patient pour les tests."""
        self.patient = CustomUser.objects.create_user(
            username="patient_test",
            email="patient@test.fr",
            password="password123",
            role=CustomUser.Role.PATIENT
        )

    def test_calcul_score_who5_nominal(self):
        """
        Vérifie le calcul correct du score brut et du score sur 100 pour des réponses nominales.
        Exemple : 4 + 3 + 4 + 3 + 4 = 18 -> Score sur 100 = 18 * 4 = 72.
        """
        eval_obj = Evaluation(
            patient=self.patient,
            reponseQ1=4,
            reponseQ2=3,
            reponseQ3=4,
            reponseQ4=3,
            reponseQ5=4,
        )
        self.assertEqual(eval_obj.calculerScoreTotal(), 18)
        self.assertEqual(eval_obj.calculerScoreSur100(), 72)

    def test_calcul_score_who5_extremes(self):
        """
        Vérifie les scores aux deux bornes extrêmes (minimum = 0, maximum = 100).
        """
        # Score minimal (toutes les réponses à 0)
        eval_min = Evaluation(
            patient=self.patient,
            reponseQ1=0, reponseQ2=0, reponseQ3=0, reponseQ4=0, reponseQ5=0
        )
        self.assertEqual(eval_min.calculerScoreTotal(), 0)
        self.assertEqual(eval_min.calculerScoreSur100(), 0)

        # Score maximal (toutes les réponses à 5)
        eval_max = Evaluation(
            patient=self.patient,
            reponseQ1=5, reponseQ2=5, reponseQ3=5, reponseQ4=5, reponseQ5=5
        )
        self.assertEqual(eval_max.calculerScoreTotal(), 25)
        self.assertEqual(eval_max.calculerScoreSur100(), 100)

    def test_sauvegarde_automatique_des_scores(self):
        """
        Vérifie que la méthode save() met bien à jour scoreBrut et scoreSur100 en base de données.
        """
        eval_obj = Evaluation.objects.create(
            patient=self.patient,
            reponseQ1=5,
            reponseQ2=4,
            reponseQ3=3,
            reponseQ4=2,
            reponseQ5=1
        )
        # Somme = 15, Score 100 = 60
        self.assertEqual(eval_obj.scoreBrut, 15)
        self.assertEqual(eval_obj.scoreSur100, 60)
