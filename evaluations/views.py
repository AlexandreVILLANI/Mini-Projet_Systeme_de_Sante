"""
evaluations/views.py : Vues pour le questionnaire WHO-5, les résultats et l'historique.
Connecté au modèle open source Qwen3-4B via Ollama.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

from .services import ServiceIA_Ollama
from .models import PlanPedagogique

# Questions officielles WHO-5 de l'Organisation Mondiale de la Santé
# (Ces questions sont officielles et fixes, elles sont À GARDER pour le projet)
QUESTIONS_WHO5 = [
    {
        "id": 1,
        "texte": "Je me suis senti(e) gai(e) et de bonne humeur"
    },
    {
        "id": 2,
        "texte": "Je me suis senti(e) calme et détendu(e)"
    },
    {
        "id": 3,
        "texte": "Je me suis senti(e) actif/ve et vigoureux/se"
    },
    {
        "id": 4,
        "texte": "Je me suis réveillé(e) frais/fraîche et dispos(e)"
    },
    {
        "id": 5,
        "texte": "Ma vie quotidienne a été remplie de choses qui m'intéressent"
    },
]

# Échelle de Likert officielle (0 à 5) - À GARDER pour le projet
ECHELLE_LIKERT = [
    {"valeur": 5, "libelle": "Tout le temps"},
    {"valeur": 4, "libelle": "La plupart du temps"},
    {"valeur": 3, "libelle": "Plus de la moitié du temps"},
    {"valeur": 2, "libelle": "Moins de la moitié du temps"},
    {"valeur": 1, "libelle": "De temps en temps"},
    {"valeur": 0, "libelle": "À aucun moment"},
]


def vue_questionnaire(request):
    """Affiche et traite le questionnaire officiel WHO-5 en interrogeant Qwen3-4B."""
    if request.method == 'POST':
        # Récupération et calcul du score officiel OMS
        reponses = []
        for i in range(1, 6):
            val = request.POST.get(f'q{i}')
            reponses.append(int(val) if val is not None else 3)

        score_brut = sum(reponses)
        score_100 = score_brut * 4

        # Connexion avec le Service LLM Ollama (Qwen3-4B)
        service_ia = ServiceIA_Ollama(modele="qwen3:4b")
        analyse_score = service_ia.analyserScore(score_100)
        texte_plan = service_ia.genererPlan7Jours(score_100)

        # =========================================================================
        # [TEMPORAIRE - NE PAS GARDER POUR LA VERSION FINALE DU PROJET]
        # Ce stockage dans la session HTTP sert pour la démo courante.
        # TODO FINALE :
        # 1. Remplacer par l'enregistrement de l'objet Evaluation et PlanPedagogique en BDD :
        #    nouvelle_eval = Evaluation.objects.create(
        #        patient=request.user,
        #        reponseQ1=reponses[0], reponseQ2=reponses[1], reponseQ3=reponses[2],
        #        reponseQ4=reponses[3], reponseQ5=reponses[4]
        #    )
        #    PlanPedagogique.objects.create(evaluation=nouvelle_eval, contenuTexte=texte_plan)
        # 2. Rediriger vers : redirect('evaluations:resultats', evaluation_id=nouvelle_eval.id)
        # =========================================================================
        request.session['dernier_score_brut'] = score_brut
        request.session['dernier_score_100'] = score_100
        request.session['dernier_analyse_score'] = analyse_score
        request.session['dernier_texte_plan'] = texte_plan

        messages.success(
            request, 
            f"Questionnaire validé avec succès ! Score WHO-5 : {score_100}/100. "
            f"Plan de bien-être analysé et généré par Qwen3-4B."
        )
        return redirect('evaluations:resultats', evaluation_id=1)

    context = {
        'questions': QUESTIONS_WHO5,
        'echelle': ECHELLE_LIKERT,
    }
    return render(request, 'evaluations/questionnaire.html', context)


def vue_resultats(request, evaluation_id=1):
    """Présentation des résultats et de la réponse textuelle produite par Qwen3-4B."""
    score_brut = request.session.get('dernier_score_brut', 18)
    score_100 = request.session.get('dernier_score_100', 72)
    analyse_score = request.session.get('dernier_analyse_score')
    texte_plan = request.session.get('dernier_texte_plan')

    # Si accès direct sans session préalable, on interroge Qwen3-4B
    if not texte_plan:
        service_ia = ServiceIA_Ollama(modele="qwen3:4b")
        analyse_score = service_ia.analyserScore(score_100)
        texte_plan = service_ia.genererPlan7Jours(score_100)

    context = {
        'evaluation_id': evaluation_id,
        'date_evaluation': datetime.now().strftime("%d/%m/%Y"),
        'score_brut': score_brut,
        'score_100': score_100,
        'analyse_score': analyse_score,
        'texte_plan': texte_plan,
        'modele_ia': "Qwen3-4B (via Ollama local)",
        'avertissement_medical': PlanPedagogique.AVERTISSEMENT_PAR_DEFAUT,
    }
    return render(request, 'evaluations/resultats.html', context)


def vue_historique(request):
    """Consultation de l'historique des évaluations du patient."""
    # =========================================================================
    # [TEMPORAIRE - NE PAS GARDER POUR LA VERSION FINALE DU PROJET]
    # Cette liste 'historique_evaluations' contient de fausses évaluations en dur
    # pour tester l'affichage du tableau sans avoir encore créé de vrais comptes.
    # TODO FINALE :
    # 1. Remplacer par la requête ORM réelle filtrée sur le patient connecté :
    #    evaluations = Evaluation.objects.filter(patient=request.user).order_by('-dateEvaluation')
    # 2. Protéger la vue avec le décorateur @login_required pour que chaque
    #    patient ne voie QUE ses propres résultats.
    # =========================================================================
    historique_evaluations = [
        {
            "id": 1,
            "date": "06/11/2026",
            "score_brut": request.session.get('dernier_score_brut', 18),
            "score_100": request.session.get('dernier_score_100', 72),
            "niveau": "Bien-être satisfaisant"
        },
        {
            "id": 2,
            "date": "23/10/2026",
            "score_brut": 14,
            "score_100": 56,
            "niveau": "Bien-être modéré"
        },
        {
            "id": 3,
            "date": "09/10/2026",
            "score_brut": 11,
            "score_100": 44,
            "niveau": "Vigilance bien-être"
        },
    ]

    context = {
        'evaluations': historique_evaluations,
    }
    return render(request, 'evaluations/historique.html', context)
