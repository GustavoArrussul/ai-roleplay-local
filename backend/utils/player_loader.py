import os
import json
from backend.config import STORY_DIR


def load_player_profile():
    player_file = os.path.join(STORY_DIR, "player.json")
    default_data = {
        "default_name": "Anon",
        "age": 20,
        "height": "1.80m",
        "hair_color": "preto",
        "description": "Um jovem de 20 anos, 1.80m de altura, cabelo preto."
    }

    if os.path.exists(player_file):
        try:
            with open(player_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar player.json: {e}")
    return default_data