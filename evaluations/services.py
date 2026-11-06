"""
evaluations/services.py : Service d'intégration du LLM (Ollama) et plan de secours.

Conforme au diagramme de classes UML :
- Classe 'ServiceIA_Ollama'
- Attributs :
    * modele : String = "qwen3:4b" (Qwen3-4B via Ollama)
    * urlApi : String = "http://localhost:11434/api/generate"
    * systemPrompt : String
- Méthodes :
    * analyserScore(score: int) -> String
    * genererPlan7Jours(score: int) -> String (ou PlanPedagogique)
- Exigences du cahier des charges :
    * Analyser le score WHO-5 et proposer un plan pédagogique de bien-être sur 7 jours.
    * Réponse de secours (fallback) si le LLM est indisponible.
    * Interdiction formelle des recommandations et diagnostics médicaux.
"""
import re
import requests
from typing import Dict, List, Any


class ServiceIA_Ollama:
    """
    Connecteur vers le modèle de langage open source Qwen3-4B exécuté localement avec Ollama.
    """

    def __init__(
        self,
        modele: str = "qwen3:4b",
        url_api: str = "http://localhost:11434/api/generate"
    ):
        self.modele = modele
        self.urlApi = url_api
        
        # Garde-fou éthique et légal obligatoire (Cahier des charges)
        self.systemPrompt = (
            "Tu es un assistant éducatif bienveillant spécialisé dans le bien-être au quotidien pour l'application WellMind-Lab. "
            "RÈGLE ABSOLUE ET STRICTE : Tu n'es pas médecin. Tu ne dois JAMAIS poser de diagnostic médical, "
            "ni qualifier un état de maladie ou pathologie clinique (ex: dépression, anxiété clinique), "
            "ni prescrire de médicament ou de traitement médical. "
            "À partir du score WHO-5 fourni (sur 100), rédige une brève analyse pédagogique et un plan éducatif "
            "structuré sur exactement 7 jours (Jour 1 à Jour 7). "
            "Pour chaque jour, donne un conseil accessible, concret et positif (respiration, marche, sommeil, gratitude, lien social, créativité, bilan). "
            "Reste encourageant, concis et bienveillant."
        )

    def analyserScore(self, score_100: int) -> str:
        """
        Fournit une explication pédagogique du score obtenu sans diagnostic clinique.
        """
        if score_100 >= 70:
            return "Indice de bien-être élevé : bon équilibre général observé au cours des deux dernières semaines."
        elif score_100 >= 50:
            return "Indice de bien-être moyen : niveau satisfaisant avec des pistes d'amélioration pour prendre soin de vous."
        else:
            return "Indice de bien-être en vigilance : une période qui semble plus exigeante, invitant au repos et à l'écoute de soi."

    # Alias snake_case
    analyser_score = analyserScore

    def genererPlan7Jours(self, score_100: int) -> str:
        """
        Interroge Ollama avec le modèle Qwen3-4B pour générer le plan sur 7 jours.
        En cas d'erreur ou d'indisponibilité, bascule immédiatement sur le plan de secours.
        """
        analyse = self.analyserScore(score_100)
        user_prompt = (
            f"L'utilisateur a complété le questionnaire officiel WHO-5 de l'OMS.\n"
            f"Score calculé : {score_100} / 100.\n"
            f"Tendance : {analyse}\n\n"
            f"Rédige le plan pédagogique de bien-être structuré sur 7 jours (Jour 1 à Jour 7) "
            f"avec pour chaque jour une action concrète et bienveillante."
        )

        payload = {
            "model": self.modele,
            "prompt": user_prompt,
            "system": self.systemPrompt,
            "stream": False,
            "options": {
                "temperature": 0.6,
                "top_p": 0.9,
            }
        }

        try:
            # Appel HTTP vers le serveur Ollama local
            response = requests.post(self.urlApi, json=payload, timeout=25)
            
            if response.status_code == 200:
                data = response.json()
                texte_genere = data.get("response", "").strip()
                if texte_genere:
                    return texte_genere

            # Si le code HTTP n'est pas 200, bascule sur la réponse de secours
            return self._plan_de_secours(score_100)

        except (requests.exceptions.RequestException, Exception):
            # Si Ollama est arrêté, timeout ou erreur réseau : plan de secours
            return self._plan_de_secours(score_100)

    # Alias snake_case
    generer_plan_7_jours = genererPlan7Jours

    def extraire_jours(self, texte_plan: str) -> List[Dict[str, Any]]:
        """
        Extrait les 7 jours sous forme de liste structurée pour l'affichage visuel,
        ou renvoie un découpage propre par défaut.
        """
        jours = []
        # Recherche des motifs 'Jour 1', 'Jour 2', etc.
        pattern = r"(?:(?:###?\s*)?Jour\s*(\d)\s*[:\-–]?\s*([^\n\r]+)?)([\s\S]*?)(?=(?:###?\s*)?Jour\s*\d|\Z)"
        matches = list(re.finditer(pattern, texte_plan, re.IGNORECASE))

        if len(matches) >= 5:
            for m in matches[:7]:
                num_jour = m.group(1)
                titre = (m.group(2) or "").strip().strip("*: -")
                contenu = m.group(3).strip()
                # Nettoyage Markdown de base
                contenu = re.sub(r"^\*+|\*+$", "", contenu).strip()
                if not titre:
                    titre = f"Étape du jour {num_jour}"
                jours.append({
                    "jour": int(num_jour),
                    "titre": titre,
                    "contenu": contenu or "Action de bien-être recommandée pour aujourd'hui."
                })
            return jours

        # Découpage par défaut si le texte est sous forme de liste ou de paragraphes
        lignes = [l.strip() for l in texte_plan.split("\n") if l.strip() and not l.startswith("#")]
        for idx in range(1, 8):
            contenu = lignes[idx - 1] if idx - 1 < len(lignes) else "Accordez-vous un moment de calme et de détente."
            jours.append({
                "jour": idx,
                "titre": f"Jour {idx}",
                "contenu": contenu
            })
        return jours

    def _plan_de_secours(self, score_100: int) -> str:
        """
        Plan pédagogique standard de secours (Fallback) exigé par le sujet du TP.
        Garantit qu'une réponse bienveillante est toujours fournie même sans Ollama.
        """
        analyse = self.analyserScore(score_100)
        return (
            f"### Plan Pédagogique de Bien-Être sur 7 Jours (Mode secours - LLM indisponible)\n\n"
            f"Analyse de l'indice : {analyse}\n\n"
            f"Jour 1 : Respiration & Pause — Consacrez 5 minutes à une respiration guidée ventrale pour relâcher les tensions musculaires.\n"
            f"Jour 2 : Activité physique douce — Faites une marche de 20 minutes en extérieur à un rythme confortable.\n"
            f"Jour 3 : Sommeil et déconnexion — Éteignez tous vos écrans 45 minutes avant de vous coucher pour favoriser l'endormissement.\n"
            f"Jour 4 : Gratitude & Positif — Notez sur un carnet trois moments agréables vécus au cours de votre journée.\n"
            f"Jour 5 : Lien social bienveillant — Partagez un échange chaleureux avec un proche ou un collègue.\n"
            f"Jour 6 : Pause ressourçante — Accordez-vous un temps dédié à une activité créative ou reposante (lecture, musique).\n"
            f"Jour 7 : Bilan hebdomadaire — Faites le point avec bienveillance sur votre semaine et identifiez ce qui vous a fait du bien."
        )
