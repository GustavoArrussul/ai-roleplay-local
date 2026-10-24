import os
import time
import base64
import io
import requests
from PIL import Image
from backend.config import CHARS_DIR, FORGE_URL
from backend.utils.keywords import (
    ENVIRONMENTS, AFTER_SEX_TERMS, KEYWORD_SEX,
    KEYWORD_ORAL, KEYWORD_MASTURB, KEYWORD_CLIMAX,
    KEYWORD_ROMANCE, KEYWORD_NAKED
)


def gerar_imagem_individual(character_key, prompt_scene, char_data, user_text):
    char_img_dir = os.path.join(CHARS_DIR, character_key, "char_images")
    os.makedirs(char_img_dir, exist_ok=True)

    text_lower = user_text.lower()

    # ==========================================
    # 1. CATEGORIZAÇÃO INTELIGENTE DE CENÁRIOS
    # ==========================================
    background_tag = "indoor bedroom background"  # Padrão
    for key, tag in ENVIRONMENTS.items():
        if key in text_lower:
            background_tag = tag
            break

    # ==========================================
    # 2. CATEGORIZAÇÃO DE ESTADOS, AÇÕES E NSFW
    # ==========================================
    is_after_sex = any(term in text_lower for term in AFTER_SEX_TERMS)

    is_sex = any(word in text_lower for word in KEYWORD_SEX) and not is_after_sex
    is_oral = any(word in text_lower for word in KEYWORD_ORAL) and not is_after_sex
    is_masturb = any(word in text_lower for word in KEYWORD_MASTURB)
    is_climax = any(word in text_lower for word in KEYWORD_CLIMAX)
    is_romance = any(word in text_lower for word in KEYWORD_ROMANCE)

    is_naked = any(word in text_lower for word in KEYWORD_NAKED) or is_sex or is_oral or is_masturb or is_climax

    # ==========================================
    # 3. ATRIBUIÇÃO DE TAGS DE ROUPA E COMPOSIÇÃO
    # ==========================================
    if is_oral:
        clothing_tag = "nude, uncensored, explicit, kneeling, oral, fellatio, penis in mouth, intimate"
        solo_tag = "1girl, couple"
        negative_clothing_tag = ", clothed, dress, shirt, pants, skirt, uniform, kimono, panties, bra"
    elif is_sex:
        if is_climax:
            clothing_tag = "nude, uncensored, explicit, missionary, laying, on back, bed, body to body, intimate, climax, cum on body"
        else:
            clothing_tag = "nude, uncensored, explicit, missionary, laying, on back, bed, body to body, intimate"
        solo_tag = "1girl, couple"
        negative_clothing_tag = ", clothed, dress, shirt, pants, skirt, uniform, kimono, panties, bra"
    elif is_masturb:
        clothing_tag = "nude, solo, touching self, arousal, bed, spreading legs"
        solo_tag = "1girl, solo"
        negative_clothing_tag = ", clothed, dress, shirt, pants, skirt, uniform, kimono, panties, bra"
    elif is_romance:
        clothing_tag = "casual clothes, embracing, kissing, close to each other, romantic"
        solo_tag = "1girl, couple"
        negative_clothing_tag = ", nude, naked"
    elif is_naked or is_after_sex:
        clothing_tag = "nude, solo, exposed body, indoor, relaxed"
        solo_tag = "1girl, solo"
        negative_clothing_tag = ", clothed, dress, shirt, pants, skirt, uniform, kimono, panties, bra, underwear"
    else:
        if "Nezuko" in character_key:
            clothing_tag = "pink kimono, checkered sash, wide sleeves"
        elif "Momo" in character_key:
            clothing_tag = "casual clothes"
        else:
            clothing_tag = "school uniform, long-sleeved shirt, pleated skirt"
        solo_tag = "1girl, solo"
        negative_clothing_tag = ", nude, naked, nipples, breasts out"

    # ==========================================
    # 4. SELEÇÃO DO LORA DA PERSONAGEM
    # ==========================================
    if "Momo" in character_key:
        lora_tag = "<lora:momo-yaoyorozu-ponyxl-lora-nochekaiser:0.9>"
    elif "Nezuko" in character_key:
        lora_tag = "<lora:nezuko-kamado-anime-ponyxl-lora-nochekaiser:0.9>"
    else:
        lora_tag = "<lora:mina-ashido-anime-ponyxl-lora-nochekaiser:0.8>"

    # ==========================================
    # 5. MONTAGEM FINAL DOS PROMPTS
    # ==========================================
    quality_tags = "score_9, score_8_up, score_7_up, masterpiece, high quality, absurdres, detailed skin"
    style_tags = "anime style, 2d illustration, modern anime aesthetic, clean lines"
    appearance = char_data.get('appearance', '')

    final_prompt = (
        f"{quality_tags}, {style_tags}, {lora_tag}, {appearance}, "
        f"{clothing_tag}, {prompt_scene}, {background_tag}, {solo_tag}"
    )

    final_negative = (
        f"lowres, bad anatomy, bad hands, text, error, blurry, extra limbs, deformed, bad proportions, "
        f"score_6, score_5, score_4, source_furry, photorealistic, realistic, photo, 3d render{negative_clothing_tag}"
    )

    payload = {
        "prompt": final_prompt,
        "negative_prompt": final_negative,
        "steps": 26,
        "width": 768,
        "height": 1024,
        "cfg_scale": 6.5,
        "sampler_name": "DPM++ 2M Karras",
        "override_settings": {
            "sd_model_checkpoint": "ponyDiffusionV6XL_v6StartWithThisOne"
        }
    }

    try:
        response = requests.post(f"{FORGE_URL}/sdapi/v1/txt2img", json=payload, timeout=180)
        if response.status_code == 200:
            r = response.json()
            for image_data in r['images']:
                image = Image.open(io.BytesIO(base64.b64decode(image_data.split(",", 1)[0])))
                filename = f"scene_{int(time.time())}.png"
                caminho_arquivo = os.path.join(char_img_dir, filename)
                image.save(caminho_arquivo)
                return f"/saves/minha_primeira_historia/characters/{character_key}/char_images/{filename}"
    except Exception as e:
        print(f"Erro ao comunicar com o Forge: {e}")
    return None