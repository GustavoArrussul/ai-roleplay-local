import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.config import BASE_DIR
from backend.services.chat_service import handle_chat, ChatRequest
from backend.services.image_service import gerar_imagem_individual

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    target_char_key, char_real_name, char_data, ai_reply = handle_chat(request)
    img_url = gerar_imagem_individual(target_char_key, request.prompt, char_data, request.prompt)

    return {
        "response": ai_reply,
        "image": img_url,
        "character_name": char_real_name
    }

app.mount("/saves", StaticFiles(directory=os.path.join(BASE_DIR, "saves")), name="saves")

frontend_dir = os.path.join(BASE_DIR, "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)