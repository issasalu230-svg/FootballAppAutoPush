# app_football_auto_push.py

import requests
import json
import time
import os

# -------------------
# CONFIGURATION
# -------------------
API_URL = "https://exemple.com/api/matchs"  # Remplace par l'URL de ton API
API_TOKEN = "votre_token_ici"
PUSH_ENDPOINT = "https://exemple.com/api/push"
INTERVALLE = 300  # 300 secondes = 5 minutes
MEMOIRE_FILE = "matchs_envoyes.json"

# -------------------
# CHARGER LES MATCHS ENVOYÉS
# -------------------
if os.path.exists(MEMOIRE_FILE):
    with open(MEMOIRE_FILE, "r") as f:
        matchs_envoyes = set(json.load(f))
else:
    matchs_envoyes = set()

# -------------------
# FONCTIONS PRINCIPALES
# -------------------

def get_matchs():
    """Récupère les matchs depuis l'API."""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("matchs", [])  # Adapter selon la structure de ton API
    except Exception as e:
        print(f"Erreur lors de la récupération des matchs : {e}")
        return []

def push_notification(match):
    """Envoie une notification pour un match."""
    payload = {
        "title": f"Match à venir : {match['equipe1']} vs {match['equipe2']}",
        "message": f"Heure : {match['heure']}, Stade : {match['stade']}"
    }
    try:
        response = requests.post(PUSH_ENDPOINT, json=payload)
        response.raise_for_status()
        print(f"Notification envoyée pour {match['equipe1']} vs {match['equipe2']}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de la notification : {e}")

def sauvegarder_matchs_envoyes():
    """Sauvegarde les matchs déjà envoyés dans un fichier."""
    with open(MEMOIRE_FILE, "w") as f:
        json.dump(list(matchs_envoyes), f)

# -------------------
# BOUCLE PRINCIPALE AUTO-PUSH
# -------------------

def main():
    global matchs_envoyes
    while True:
        matchs = get_matchs()
        if matchs:
            for match in matchs:
                match_id = match.get("id")  # Chaque match doit avoir un ID unique
                if match_id not in matchs_envoyes:
                    push_notification(match)
                    matchs_envoyes.add(match_id)
                    sauvegarder_matchs_envoyes()
        else:
            print("Aucun match trouvé.")
        
        print(f"Attente de {INTERVALLE} secondes avant la prochaine vérification...")
        time.sleep(INTERVALLE)

# Point d'entrée
if __name__ == "__main__":
    main()
