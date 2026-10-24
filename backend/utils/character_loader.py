import os
import json
from backend.config import CHARS_DIR


def load_dynamic_characters():
    characters = {}
    if not os.path.exists(CHARS_DIR):
        return characters
    for char_folder in os.listdir(CHARS_DIR):
        char_path = os.path.join(CHARS_DIR, char_folder)
        if os.path.isdir(char_path):
            profile_file = os.path.join(char_path, "profile.json")
            if os.path.exists(profile_file):
                try:
                    with open(profile_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        characters[char_folder] = data
                except Exception as e:
                    print(f"Erro ao carregar perfil de {char_folder}: {e}")
    return characters


def resolve_target_character(user_prompt: str, all_chars: dict, last_active: str) -> str:
    user_prompt_lower = user_prompt.lower()
    personagens_mencionadas = []

    for key, data in all_chars.items():
        char_name = data.get("name", "").lower()
        folder_clean = key.lower().replace("_", " ")
        if folder_clean in user_prompt_lower or char_name in user_prompt_lower or key.lower() in user_prompt_lower:
            personagens_mencionadas.append(key)

    if len(personagens_mencionadas) == 1:
        return personagens_mencionadas[0]
    elif len(personagens_mencionadas) >= 2:
        return personagens_mencionadas[-1]  # Última citada tem prioridade
    else:
        return last_active