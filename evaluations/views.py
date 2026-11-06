"""
evaluations/views.py : Vues pour le questionnaire WHO-5, les résultats et l'historique.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

# Questions officielles WHO-5 de l'Organisation Mondiale de la Santé
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

ECHELLE_LIKERT = [
    {"valeur": 5, "libelle": "Tout le temps"},
    {"valeur": 4, "libelle": "La plupart du temps"},
    {"valeur": 3, "libelle": "Plus de la moitié du temps"},
    {"valeur": 2, "libelle": "Moins de la moitié du temps"},
    {"valeur": 1, "libelle": "De temps en temps"},
    {"valeur": 0, "libelle": "À aucun moment"},
]


def vue_questionnaire(request):
    """Affiche et traite le questionnaire officiel WHO-5."""
    if request.method == 'POST':
        # Récupération et calcul du score
        reponses = []
        for i in range(1, 6):
            val = request.POST.get(f'q{i}')
            reponses.append(int(val) if val is not None else 3)

        score_brut = sum(reponses)
        score_100 = score_brut * 4

        # Enregistrement en session pour la démo front-end
        request.session['dernier_score_brut'] = score_brut
        request.session['dernier_score_100'] = score_100
        messages.success(request, f"Votre questionnaire a été validé avec succès ! Score : {score_100}/100")
        return redirect('evaluations:resultats', evaluation_id=1)

    context = {
        'questions': QUESTIONS_WHO5,
        'echelle': ECHELLE_LIKERT,
    }
    return render(request, 'evaluations/questionnaire.html', context)


def vue_resultats(request, evaluation_id=1):
    """Présentation des résultats et du plan pédagogique sur 7 jours."""
    score_brut = request.session.get('dernier_score_brut', 17)
    score_100 = request.session.get('dernier_score_100', 68)

    # Exemple de plan pédagogique 7 jours généré (simulé pour l'affichage front-end)
    plan_7_jours = [
        {"jour": 1, "titre": "Prise de conscience & Respiration", "contenu": "Consacrez 5 minutes à une respiration guidée en pleine conscience pour relâcher les tensions musculaires."},
        {"jour": 2, "titre": "Activité physique douce", "contenu": "Faites une marche de 20 minutes en extérieur à un rythme confortable pour stimuler votre énergie."},
        {"jour": 3, "titre": "Déconnexion numérique", "contenu": "Éteignez tous les écrans (téléphone, ordinateur) 45 minutes avant de vous coucher pour favoriser l'endormissement."},
        {"jour": 4, "titre": "Reconnaissance et gratitude", "contenu": "Notez sur un carnet trois moments positifs ou agréables vécus au cours de votre journée."},
        {"jour": 5, "titre": "Lien social bienveillant", "contenu": "Partagez un moment d'échange chaleureux (appel, café) avec un proche ou un collègue."},
        {"jour": 6, "titre": "Pause créative ou ressourçante", "contenu": "Accordez-vous 30 minutes dédiées à une passion non liée au travail (lecture, musique, dessin)."},
        {"jour": 7, "titre": "Bilan & Bienveillance", "contenu": "Prenez le temps de faire le point sur votre semaine sans jugement et identifiez ce qui vous a fait le plus de bien."}
    ]

    avertissement_medical = (
        "Cet outil est conçu exclusivement à des fins pédagogiques et éducatives avec des données fictives. "
        "Les conseils présentés ne constituent en aucun cas un diagnostic médical ni une prescription thérapeutique. "
        "En cas de souffrance psychologique ou de détresse, consultez un professionnel de santé qualifié."
    )

    context = {
        'evaluation_id': evaluation_id,
        'date_evaluation': datetime.now().strftime("%d/%m/%Y"),
        'score_brut': score_brut,
        'score_100': score_100,
        'plan_7_jours': plan_7_jours,
        'avertissement_medical': avertissement_medical,
    }
    return render(request, 'evaluations/resultats.html', context)


def vue_historique(request):
    """Consultation de l'historique des évaluations du patient."""
    # Données simulées pour la démo front-end
    historique_evaluations = [
        {
            "id": 1,
            "date": "06/11/2026",
            "score_brut": request.session.get('dernier_score_brut', 17),
            "score_100": request.session.get('dernier_score_100', 68),
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
