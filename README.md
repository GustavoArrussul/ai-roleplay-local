# Local Visual Novel & AI Story Engine

Um motor de jogo de **Visual Novel** local e automatizado, alimentado por Inteligência Artificial. O projeto combina narração em linguagem natural fluida através do **Ollama (modelo dolphin-llama3)** com geração automática de ilustrações e cenas via **Stable Diffusion Forge (modelo PonyXL)**, estruturado numa arquitetura modular baseada em **FastAPI**.

---

## 🚀 Visão Geral do Projeto

Este projeto consiste num sistema local de *Roleplay* e Visual Novel interativa. O jogador interage por chat em linguagem natural com personagens dinâmicas que mantêm a sua persona sem quebrar a 4.ª parede. O backend em **FastAPI** gere o histórico de conversas, o estado do jogador e rastreia o contexto da história, traduzindo automaticamente os acontecimentos narrativos em prompts visuais para o gerador de imagem.

---

## 🛠️ Arquitetura Modular

O projeto está organizado de forma modular para facilitar a manutenção e a escalabilidade:

* **`chat_service.py`**: Gere a comunicação direta com a API do Ollama (`/api/chat`), garantindo que o modelo assume corretamente a persona da personagem, respeita o contexto geográfico e mantém um fluxo de diálogo orgânico.
* **`image_service.py`**: Responsável por processar o contexto e comunicar com a API do Stable Diffusion Forge para desenhar as ilustrações das cenas em tempo de execução.
* **`keywords.py`**: Traduz os eventos e o cenário da narrativa atual em palavras-chave visuais otimizadas para a geração de imagens.
* **`character_loader.py` & `player_loader.py`**: Carregam dinamicamente perfis, traços de personalidade, estatísticas e dados estruturados de ficheiros locais.

---

## 🎨 Integração com o Stable Diffusion Forge

O motor utiliza o **Stable Diffusion Forge** como diretor de arte automatizado, com especificações otimizadas:
* **Modelo Base**: Desenvolvido a pensar nativamente em **PonyXL**.
* **Resolução Otimizada**: Utiliza resoluções verticais de retrato (como `768x1024`) para assegurar uma proporção ideal de Visual Novel e corrigir problemas de assimetria anatómica.
* **Parâmetros de Amostragem**: Utiliza o sampler `DPM++ 2M Karras` configurado a cerca de **22 passos**, garantindo um excelente equilíbrio entre tempo de renderização (evitando o consumo excessivo de VRAM) e alta qualidade visual.
* **Consistência**: Integração de LoRAs específicos por personagem para garantir consistência visual nas ilustrações geradas.

---

## ⚙️ Pré-requisitos e Requisitos de Sistema

Para executar este projeto localmente, vais precisar de ter instalado no teu computador:

1. **Python 3.10+** (para correr o backend em FastAPI).
2. **Ollama** a correr localmente na porta padrão (`http://localhost:11434`) com o modelo instalado:
   ```bash
   ollama run dolphin-llama3
   ```
3. **Stable Diffusion Forge** (ou WebUI equivalente) a correr localmente na porta padrão (`http://127.0.0.1:7860`), com a **API ativada** (através do argumento `--api`), utilizando um checkpoint compatível com **PonyXL** e os respetivos LoRAs das personagens.

---

## 📥 Instalação e Execução

Segue os passos abaixo para colocar o projeto a funcionar na tua máquina:

1. **Clona o repositório**:
   ```bash
   git clone https://github.com/GustavoArrussul/ai-roleplay-local.git
   cd ai-roleplay-local
   ```

2. **Instala as dependências do Python**:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Inicia o servidor backend (FastAPI)**:
   ```bash
   python backend/main.py
   ```

4. **Abre a interface**:
   Acede ao frontend no teu navegador web para começar a interagir com as tuas histórias e personagens!