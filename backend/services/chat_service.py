import requests
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.utils.character_loader import load_dynamic_characters, resolve_target_character
from backend.utils.player_loader import load_player_profile

last_active_character = "Mina_Ashido"
current_environment_context = "banheiro"


class ChatRequest(BaseModel):
    prompt: str
    player_name: Optional[str] = None


def handle_chat(request: ChatRequest):
    global last_active_character, current_environment_context
    ollama_url = "http://localhost:11434/api/chat"  # Mudado para a rota /api/chat que suporta mensagens estruturadas
    all_chars = load_dynamic_characters()
    player_data = load_player_profile()

    if not all_chars:
        raise HTTPException(status_code=404, detail="Nenhuma personagem encontrada.")

    player_name = request.player_name if request.player_name else player_data.get("default_name", "Anon")

    target_char_key = resolve_target_character(request.prompt, all_chars, last_active_character)
    last_active_character = target_char_key

    char_data = all_chars[target_char_key]
    char_real_name = char_data.get('name', target_char_key)
    char_appearance = char_data.get('appearance', '')
    char_personality = char_data.get('personality', '')

    # Deteta se o utilizador mudou de ambiente
    text_lower = request.prompt.lower()
    environments_map = ["banheiro", "quarto", "cozinha", "sala", "rua", "escola", "floresta", "praia", "piscina",
                        "varanda"]
    for env in environments_map:
        if env in text_lower:
            current_environment_context = env
            break

    # Usando a estrutura oficial de mensagens do Ollama (System + User)
    messages = [
        {
            "role": "system",
            "content": (
                f"Você é unicamente e exclusivamente a personagem de ficção chamada {char_real_name}. "
                f"Personalidade: {char_personality}. Aparência: {char_appearance}. "
                f"Localização atual: {current_environment_context}. "
                f"O utilizador é {player_name} (homem). "
                f"REGRA ABSOLUTA DE NATURALIDADE: Fale, reaja e dialogue de forma 100% natural, humana e orgânica. "
                f"NUNCA quebre a 4ª parede. NUNCA mencione termos como 'romance visual', 'jogo', 'ficção', 'script', 'narrativa' ou 'IA'. "
                f"Converse exatamente como uma pessoa real conversaria nessa situação, com emoções genuínas, reações espontâneas, sem formalidades robóticas, e coloque todas as falas entre aspas duplas. "
                f"Responda estritamente em Português do Brasil."
            )
        },
        {
            "role": "user",
            "content": f"Ação de {player_name}: {request.prompt}"
        }
    ]

    payload = {
        "model": "dolphin-llama3",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 300
        }
    }

    try:
        response = requests.post(ollama_url, json=payload, timeout=60)
        data = response.json()
        # Na rota /api/chat, a resposta vem dentro de message -> content
        ai_reply = data.get("message", {}).get("content", "Erro ao gerar resposta.").strip()
        return target_char_key, char_real_name, char_data, ai_reply
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))