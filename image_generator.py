import base64
import io
import requests
from PIL import Image

# URL da API do Forge rodando localmente
URL = "http://127.0.0.1:7860"


def gerar_imagem_via_api(prompt_texto, negative_prompt=""):
    payload = {
        "prompt": prompt_texto,
        "negative_prompt": negative_prompt,
        "steps": 25,
        "width": 1024,  # Recomendado para modelos SDXL (Anything XL)
        "height": 1024,
        "cfg_scale": 7.0,
        "sampler_name": "Euler a",
    }

    response = requests.post(f"{URL}/sdapi/v1/txt2img", json=payload)

    if response.status_code == 200:
        r = response.json()
        for i, image_data in enumerate(r['images']):
            # Descodifica a imagem em base64 recebida da API
            image = Image.open(io.BytesIO(base64.b64decode(image_data.split(",", 1)[0])))

            # Guarda a imagem localmente ou envia para o chat
            caminho_arquivo = f"output_{i}.png"
            image.save(caminho_arquivo)
            print(f"Imagem guardada com sucesso em: {caminho_arquivo}")
            return caminho_arquivo
    else:
        print(f"Erro na API: {response.status_code} - {response.text}")
        return None


# Exemplo de teste:
if __name__ == "__main__":
    gerar_imagem_via_api(
        prompt_texto="masterpiece, best quality, 1girl, cute, anime style",
        negative_prompt="lowres, bad anatomy, bad hands, text, error"
    )