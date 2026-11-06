"""
evaluations/services.py : Service d'intégration du LLM (Ollama) et plan de secours.

Rôle dans le projet :
- Classe 'ServiceIA_Ollama' (conforme au diagramme UML) :
    * Attributs : modele (ex: "Qwen3-4B"), urlApi, systemPrompt.
    * Méthode 'analyserScore(score: int) -> str' : Prépare l'analyse du score.
    * Méthode 'genererPlan7Jours(score: int) -> PlanPedagogique' : Envoie la requête HTTP à Ollama.
    * Système de secours (fallback) : si Ollama est injoignable, génère un plan bienveillant par défaut
      tout en garantissant l'absence totale de diagnostic médical.
"""

