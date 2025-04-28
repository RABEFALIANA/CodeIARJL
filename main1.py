import os
import requests
from dotenv import load_dotenv
from PyPDF2 import PdfReader

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
        text += page.extract_text() + "\n"
    return text.strip()

def build_summary_prompt(pdf_text):
    return f"Voici un document :\n\n{pdf_text}\n\nPeux-tu en faire un résumé clair et concis en français ?"

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

def summarize_pdf(pdf_filename):
    api_key = load_api_key()
    model_name = "qwen-qwq-32b"
    pdf_path = os.path.join("data", pdf_filename)

    print(f"📄 Lecture du fichier : {pdf_path}")
    pdf_text = extract_text_from_pdf(pdf_path)

    if not pdf_text:
        raise ValueError("Le fichier PDF est vide ou illisible.")

    user_prompt = build_summary_prompt(pdf_text)
    print(f"🔍 Modèle utilisé : {model_name}")
    print(f"📝 Résumé en cours...\n")

    response_json = send_request(api_key, model_name, user_prompt)
    assistant_reply = response_json["choices"][0]["message"]["content"]

    print("🧠 Résumé généré :")
    print(assistant_reply)

def main():
    pdf_filename = "entretien.pdf"  # <<< Remplace par ton nom de fichier dans /data
    summarize_pdf(pdf_filename)

if __name__ == "__main__":
    main()
