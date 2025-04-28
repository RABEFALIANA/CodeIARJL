import os
import requests
from dotenv import load_dotenv
from PyPDF2 import PdfReader

MAX_TOKENS = 4000  # Limite pour rester sous 6000 tokens avec marge

def load_api_key():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("La clé API GROQ est manquante dans le fichier .env.")
    return api_key

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text.strip()

def split_text(text, max_words=1500):
    """Découpe le texte en morceaux de taille raisonnable."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)
    return chunks

def build_themes_prompt(text_chunk):
    prompt = (
        "Voici un extrait d'entretien :\n\n"
        f"{text_chunk}\n\n"
        "Peux-tu dégager les thématiques principales abordées dans cet extrait ? "
        "Présente-les sous forme de liste en français."
    )
    return prompt

def send_request(api_key, model_name, user_prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Erreur {response.status_code} : {response.text}")
    return response.json()

def analyze_themes_in_pdf(pdf_filename):
    api_key = load_api_key()
    model_name = "qwen-qwq-32b"  # Ton modèle accessible !
    pdf_path = os.path.join("data", pdf_filename)

    print(f"📄 Lecture du fichier : {pdf_path}")
    pdf_text = extract_text_from_pdf(pdf_path)

    if not pdf_text:
        raise ValueError("Le fichier PDF est vide ou illisible.")

    chunks = split_text(pdf_text)
    print(f"✂️ Document découpé en {len(chunks)} morceaux.\n")

    for idx, chunk in enumerate(chunks):
        print(f"🔎 Analyse du morceau {idx + 1}/{len(chunks)}...")
        user_prompt = build_themes_prompt(chunk)
        response_json = send_request(api_key, model_name, user_prompt)
        assistant_reply = response_json["choices"][0]["message"]["content"]
        print(f"🎯 Thématiques extraites (partie {idx + 1}):")
        print(assistant_reply)
        print("\n" + "="*60 + "\n")

def main():
    pdf_filename = "entretien.pdf"  # <<< Mets ici ton nom exact
    analyze_themes_in_pdf(pdf_filename)

if __name__ == "__main__":
    main()
