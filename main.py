import os
from dotenv import load_dotenv
import requests

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("La clé API GROQ n'est pas trouvée dans le fichier .env.")

# Paramètres de la requête
url = "https://api.groq.com/openai/v1/chat/completions"  # Remplace si ton endpoint est différent
headers = {
    "Authorization": f"Bearer {groq_api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "gemma2-9b-it",  # adapte le nom du modèle si besoin
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
}

# Envoyer la requête
response = requests.post(url, headers=headers, json=payload)

# Vérifier et afficher la réponse
if response.status_code == 200:
    result = response.json()
    print("Réponse de Groq:")
    print(result["choices"][0]["message"]["content"])
else:
    print(f"Erreur {response.status_code} : {response.text}")
