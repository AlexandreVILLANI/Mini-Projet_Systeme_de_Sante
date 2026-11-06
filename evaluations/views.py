"""
evaluations/views.py : Vues pour le questionnaire WHO-5, les résultats et l'historique.
Persistance réelle en base de données et sécurisation des accès.

=== ÉTAT D'AVANCEMENT ===
[✅ FAIT] vue_questionnaire : reçoit les 5 réponses, crée un objet Evaluation en BDD,
          appelle ServiceIA_Ollama.genererPlan7Jours(), crée un objet PlanPedagogique en BDD.
[✅ FAIT] vue_resultats : @login_required + get_object_or_404(patient=request.user)
          → un patient ne peut jamais accéder aux résultats d'un autre.
          Appelle aussi ServiceIA_Ollama.analyserScore() pour l'analyse contextuelle du score.
[✅ FAIT] vue_historique : filtre strict Evaluation.objects.filter(patient=request.user),
          trié par date décroissante.
[✅ FAIT] QUESTIONS_WHO5 et ECHELLE_LIKERT définis comme constantes (conforme à l'UML WHO-5).

[❌ RESTE À FAIRE] Validation côté serveur des valeurs (borne 0 ≤ réponse ≤ 5) pour sécurité complète.
[❌ RESTE À FAIRE] Vues d'administration (listerComptes, ajouterCompte) si interface web dédiée
          exigée par le TP (au-delà de /admin/ Django).
[❌ RESTE À FAIRE] Pagination de l'historique si l'utilisateur a beaucoup d'évaluations.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Evaluation, PlanPedagogique
from .services import ServiceIA_Ollama

# Questions officielles WHO-5 de l'Organisation Mondiale de la Santé
QUESTIONS_WHO5 = [
    {"id": 1, "texte": "Je me suis senti(e) gai(e) et de bonne humeur"},
    {"id": 2, "texte": "Je me suis senti(e) calme et détendu(e)"},
    {"id": 3, "texte": "Je me suis senti(e) actif/ve et vigoureux/se"},
    {"id": 4, "texte": "Je me suis réveillé(e) frais/fraîche et dispos(e)"},
    {"id": 5, "texte": "Ma vie quotidienne a été remplie de choses qui m'intéressent"},
]

# Échelle de Likert officielle (0 à 5)
ECHELLE_LIKERT = [
    {"valeur": 5, "libelle": "Tout le temps"},
    {"valeur": 4, "libelle": "La plupart du temps"},
    {"valeur": 3, "libelle": "Plus de la moitié du temps"},
    {"valeur": 2, "libelle": "Moins de la moitié du temps"},
    {"valeur": 1, "libelle": "De temps en temps"},
    {"valeur": 0, "libelle": "À aucun moment"},
]


@login_required
def vue_questionnaire(request):
    """
    Affiche et traite le questionnaire WHO-5.
    Accessible uniquement aux utilisateurs authentifiés (@login_required).
    """
    if request.method == 'POST':
        # Récupération des 5 réponses (valeurs entières entre 0 et 5)
        try:
            r1 = int(request.POST.get('q1', 3))
            r2 = int(request.POST.get('q2', 3))
            r3 = int(request.POST.get('q3', 3))
            r4 = int(request.POST.get('q4', 3))
            r5 = int(request.POST.get('q5', 3))
        except (ValueError, TypeError):
            messages.error(request, "Données de formulaire invalides.")
            return redirect('evaluations:questionnaire')

        # 1. Enregistrement de l'Évaluation en base de données liée au patient connecté
        evaluation = Evaluation.objects.create(
            patient=request.user,
            reponseQ1=r1,
            reponseQ2=r2,
            reponseQ3=r3,
            reponseQ4=r4,
            reponseQ5=r5,
        )

        # 2. Appel au modèle open-source Qwen3-4B via Ollama pour générer le plan
        service_ia = ServiceIA_Ollama(modele="qwen3:4b")
        texte_plan = service_ia.genererPlan7Jours(evaluation.scoreSur100)

        # 3. Enregistrement du Plan Pédagogique lié à l'évaluation
        PlanPedagogique.objects.create(
            evaluation=evaluation,
            contenuTexte=texte_plan,
            avertissementMedical=PlanPedagogique.AVERTISSEMENT_PAR_DEFAUT
        )

        messages.success(
            request, 
            f"Votre évaluation a été enregistrée avec succès ! Score WHO-5 : {evaluation.scoreSur100}/100."
        )
        return redirect('evaluations:resultats', evaluation_id=evaluation.id)

    context = {
        'questions': QUESTIONS_WHO5,
        'echelle': ECHELLE_LIKERT,
    }
    return render(request, 'evaluations/questionnaire.html', context)


@login_required
def vue_resultats(request, evaluation_id):
    """
    Présentation des résultats et du plan pédagogique d'une évaluation précise.
    Sécurité : get_object_or_404 avec filtre patient=request.user garantit
    qu'un patient ne peut JAMAIS consulter l'évaluation d'un autre utilisateur.
    """
    evaluation = get_object_or_404(Evaluation, id=evaluation_id, patient=request.user)
    
    # Récupération du plan associé (ou génération si inexistant)
    try:
        plan = evaluation.plan
    except PlanPedagogique.DoesNotExist:
        service_ia = ServiceIA_Ollama(modele="qwen3:4b")
        texte_plan = service_ia.genererPlan7Jours(evaluation.scoreSur100)
        plan = PlanPedagogique.objects.create(
            evaluation=evaluation,
            contenuTexte=texte_plan,
            avertissementMedical=PlanPedagogique.AVERTISSEMENT_PAR_DEFAUT
        )

    # Analyse du score par l'IA
    service_ia = ServiceIA_Ollama(modele="qwen3:4b")
    analyse_score = service_ia.analyserScore(evaluation.scoreSur100)

    context = {
        'evaluation': evaluation,
        'plan': plan,
        'analyse_score': analyse_score,
        'modele_ia': "Qwen3-4B (Ollama)",
    }
    return render(request, 'evaluations/resultats.html', context)


@login_required
def vue_historique(request):
    """
    Consultation de l'historique des évaluations du patient connecté.
    Filtrage strict sur request.user conformément aux exigences de confidentialité.
    """
    evaluations = Evaluation.objects.filter(patient=request.user).order_by('-dateEvaluation')
    
    context = {
        'evaluations': evaluations,
    }
    return render(request, 'evaluations/historique.html', context)
