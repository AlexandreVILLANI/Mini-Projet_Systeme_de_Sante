"""
tests/test_ia.py : Tests unitaires Pytest pour le Service IA (Ollama) et le Fallback.

Exigences du sujet :
- Intégrer un LLM pour analyser le score et générer un plan pédagogique de bien-être sur 7 jours.
- Prévoir une réponse de secours si le LLM est indisponible.
- Empêcher formellement les recommandations et diagnostics médicaux.
"""
import pytest
from evaluations.services import ServiceIA_Ollama


def test_system_prompt_respecte_limites_medicales():
    """
    Vérifie que la consigne système (system prompt) interdit strictement tout diagnostic médical.
    """
    service = ServiceIA_Ollama()
    prompt = service.systemPrompt.lower()
    
    assert "pas médecin" in prompt or "ne dois jamais poser de diagnostic" in prompt
    assert "médical" in prompt


def test_analyse_score_selon_niveaux():
    """
    Vérifie que la méthode analyserScore fournit une appréciation cohérente selon les scores.
    """
    service = ServiceIA_Ollama()
    
    analyse_haute = service.analyserScore(80)
    assert "élevé" in analyse_haute.lower()
    
    analyse_moyenne = service.analyserScore(56)
    assert "moyen" in analyse_moyenne.lower() or "satisfaisant" in analyse_moyenne.lower()
    
    analyse_basse = service.analyserScore(32)
    assert "vigilance" in analyse_basse.lower()


def test_reponse_de_secours_fallback_si_ollama_indisponible():
    """
    Vérifie que le service ne plante pas et retourne le plan de secours si Ollama est injoignable.
    """
    # On force une URL inaccessible
    service_hors_ligne = ServiceIA_Ollama(url_api="http://localhost:99999/api/generate")
    
    # Doit s'exécuter sans lever d'exception
    plan = service_hors_ligne.genererPlan7Jours(64)
    
    assert plan is not None
    assert len(plan) > 50
    assert "secours" in plan.lower() or "jour 1" in plan.lower()


def test_extraire_jours_format_structure():
    """
    Vérifie que la méthode extraire_jours découpe le plan en 7 étapes exploitables par l'interface.
    """
    service = ServiceIA_Ollama()
    plan_brut = (
        "Jour 1 : Respiration calme\n"
        "Jour 2 : Petite marche\n"
        "Jour 3 : Sommeil réparateur\n"
        "Jour 4 : Moment de gratitude\n"
        "Jour 5 : Discussion bienveillante\n"
        "Jour 6 : Lecture relaxante\n"
        "Jour 7 : Bilan de la semaine\n"
    )
    jours = service.extraire_jours(plan_brut)
    assert len(jours) == 7
    assert jours[0]["jour"] == 1
    assert jours[6]["jour"] == 7
