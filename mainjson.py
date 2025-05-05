import os
import json

# Dossiers
input_folder = 'output_4'
output_folder = 'output_5'
os.makedirs(output_folder, exist_ok=True)

# Initialiser la structure
all_interviews = {}

# Parcourir les fichiers de output_4
for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        interview_id = filename.replace('.txt', '')
        filepath = os.path.join(input_folder, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        themes_and_verbatims = []
        current_theme = None
        current_verbatim = None
        
        for line in lines:
            line = line.strip()
            if line.startswith("Thème :"):
                if current_theme and current_verbatim:
                    themes_and_verbatims.append({
                        "theme": current_theme,
                        "verbatim": current_verbatim
                    })
                current_theme = line.replace("Thème :", "").strip()
                current_verbatim = ""
            elif line.startswith("Verbatim :"):
                current_verbatim = line.replace("Verbatim :", "").strip()
            elif current_verbatim is not None:
                current_verbatim += " " + line
        
        # Ajouter le dernier thème/verbatim
        if current_theme and current_verbatim:
            themes_and_verbatims.append({
                "theme": current_theme,
                "verbatim": current_verbatim
            })
        
        # Stocker dans la structure globale
        all_interviews[interview_id] = themes_and_verbatims

# Sauvegarder en JSON
output_path = os.path.join(output_folder, 'interviews.json')
with open(output_path, 'w', encoding='utf-8') as f_out:
    json.dump(all_interviews, f_out, ensure_ascii=False, indent=2)

print("Fichier JSON créé :", output_path)
